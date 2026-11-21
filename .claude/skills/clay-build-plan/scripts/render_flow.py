#!/usr/bin/env python3
"""Render a Clay build swimlane diagram (one lane per table, numbered steps, FREE/PAID tags) to PNG.

Usage:
    python3 render_flow.py flow.json out.png            # PNG (+ out.html next to it)
    python3 render_flow.py flow.json out.png --html-only

flow.json shape (see ../references/example-flow.json):
{
  "title": "How the PaidHR workflow moves through Clay",
  "subtitle": "Each row is a table. Follow the numbers left to right. ...",
  "lanes": [{"id": "hr", "name": "HR Leaders", "note": "one row per person. The main table.", "main": true,
             "dashed": false}, ...],                      # top to bottom
  "steps": [{"id": "s1", "n": "1", "lane": "hr", "col": 1, "title": "Find new HR leaders",
             "text": "Clay people search ...", "cost": "free" | "paid" | null, "highlight": false}, ...],
  "arrows": [{"from": "s1", "to": "s2", "label": "optional", "dashed": false}, ...]
}

Columns start at 1. Keep it to 9 columns or fewer; merge steps if you need more.
Arrows route themselves: same lane = straight right; same column = straight down/up;
otherwise an elbow from the right side of the source to the top/bottom of the target.
Needs Chrome + selenium (pip install selenium). Fonts load from Google Fonts (Rubik).
"""
import html, json, os, sys, time

THEME = dict(cream="#FFF5EE", purple="#3E0563", violet="#8B48FE", orange="#FF9600", ink="#141414",
             grey="#6B6375", line="#E4D7F2", tint="#F1E8FF", peach="#FFE7C2")

CSS = """
:root{--cream:%(cream)s;--purple:%(purple)s;--violet:%(violet)s;--orange:%(orange)s;--ink:%(ink)s;--grey:%(grey)s;--line:%(line)s;--tint:%(tint)s;--peach:%(peach)s}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1600px;background:var(--cream);font-family:Rubik,sans-serif;color:var(--ink);position:relative;padding:30px 48px 40px}
.head{display:flex;justify-content:space-between;align-items:flex-start;gap:30px}
h1{font-size:34px;font-weight:700;color:var(--purple)}
.sub{font-size:17px;color:var(--grey);margin-top:6px;max-width:1150px}
.legend{display:flex;gap:10px;align-items:center;font-size:15px;color:var(--grey);white-space:nowrap;margin-top:10px}
.tag{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.06em;padding:3px 8px;border-radius:5px}
.free{background:var(--tint);color:var(--violet)}
.paid{background:var(--peach);color:#B85F00}
.grid{display:grid;grid-template-columns:150px repeat(%(cols)d,1fr);column-gap:14px;row-gap:16px;margin-top:34px;position:relative}
.lane{grid-column:1/-1;border-radius:14px;background:#fff;border:1.5px solid var(--line);z-index:0}
.lane.dashed{border-style:dashed}
.lane.main{border:2px solid var(--violet)}
.lname{grid-column:1;align-self:center;padding:18px 0 18px 18px;z-index:2}
.lname b{display:block;font-size:18px;font-weight:700;color:var(--purple)}
.lname span{display:block;font-size:13px;color:var(--grey);margin-top:3px;line-height:1.3}
.box{z-index:3;align-self:center;margin:26px 0 22px;background:var(--cream);border:1.5px solid var(--line);border-radius:10px;padding:10px 11px 11px;position:relative}
.box .n{position:absolute;top:-12px;left:-10px;width:28px;height:28px;border-radius:50%%;background:var(--purple);color:#fff;font-weight:700;font-size:15px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #fff}
.box h3{font-size:15.5px;font-weight:600;line-height:1.2;margin:2px 0 5px 10px}
.box p{font-size:12.5px;color:var(--grey);line-height:1.35}
.box .tag{margin-top:7px}
.box.key{border-color:var(--orange);background:#FFF9F0}
svg{position:absolute;left:0;top:0;z-index:2;pointer-events:none;overflow:visible}
"""

JS = """
const s=document.getElementById('s'),V='%(violet)s',ARROWS=%(arrows)s;
function r(id){const b=document.getElementById(id).getBoundingClientRect();return{left:b.left+scrollX,right:b.right+scrollX,top:b.top+scrollY,bottom:b.bottom+scrollY,width:b.width,height:b.height}}
function path(d,dash){const p=document.createElementNS('http://www.w3.org/2000/svg','path');p.setAttribute('d',d);p.setAttribute('fill','none');p.setAttribute('stroke',V);p.setAttribute('stroke-width','2.4');p.setAttribute('marker-end','url(#a)');if(dash)p.setAttribute('stroke-dasharray','6 5');s.appendChild(p)}
function lbl(x,y,t){t.split('\\n').forEach((line,i)=>{const e=document.createElementNS('http://www.w3.org/2000/svg','text');e.setAttribute('x',x);e.setAttribute('y',y+i*17);e.setAttribute('font-family','Rubik');e.setAttribute('font-size','13');e.setAttribute('fill','%(grey)s');e.setAttribute('stroke','%(cream)s');e.setAttribute('stroke-width','5');e.setAttribute('paint-order','stroke');e.setAttribute('stroke-linejoin','round');e.textContent=line;s.appendChild(e)})}
function draw(a){const A=r(a.from),B=r(a.to),sameRow=Math.abs((A.top+A.bottom)/2-(B.top+B.bottom)/2)<40,sameCol=Math.abs((A.left+A.right)/2-(B.left+B.right)/2)<40;
 if(sameRow){const y=A.top+A.height/2,x1=B.left>A.right?A.right+2:A.left-2,x2=B.left>A.right?B.left-4:B.right+4;path(`M${x1},${y} L${x2},${y}`,a.dashed);if(a.label)lbl(Math.min(x1,x2)+4,y-8,a.label);return}
 if(sameCol){const x=A.left+A.width/2,down=B.top>A.bottom,y1=down?A.bottom+2:A.top-2,y2=down?B.top-4:B.bottom+4;path(`M${x},${y1} L${x},${y2}`,a.dashed);if(a.label)lbl(x+10,(y1+y2)/2+4,a.label);return}
 const x1=A.right+2,y1=A.top+A.height/2,x2=B.left+B.width/2,down=B.top>A.bottom,y2=down?B.top-4:B.bottom+4,k=down?12:-12;
 path(`M${x1},${y1} L${x2-12},${y1} Q${x2},${y1} ${x2},${y1+k} L${x2},${y2}`,a.dashed);if(a.label)lbl(x2+10,(y1+y2)/2,a.label)}
document.fonts.ready.then(()=>{s.setAttribute('width',document.body.scrollWidth);s.setAttribute('height',document.body.scrollHeight);ARROWS.forEach(draw);document.body.setAttribute('data-ready','1')});
"""


def build_html(spec):
    lanes, steps = spec["lanes"], spec["steps"]
    cols = max(st["col"] for st in steps)
    lane_row = {ln["id"]: i + 1 for i, ln in enumerate(lanes)}
    e = html.escape
    parts = [f'<!doctype html><html><head><meta charset="utf-8">'
             f'<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap" rel="stylesheet">'
             f'<style>{CSS % dict(THEME, cols=cols)}</style></head><body>',
             f'<div class="head"><div><h1>{e(spec["title"])}</h1><div class="sub">{e(spec.get("subtitle", ""))}</div></div>'
             f'<div class="legend"><span class="tag free">FREE</span> formulas, searches, lookups '
             f'<span class="tag paid">PAID</span> uses Actions or credits</div></div>',
             '<div class="grid">']
    for ln in lanes:
        cls = "lane" + (" main" if ln.get("main") else "") + (" dashed" if ln.get("dashed") else "")
        parts.append(f'<div class="{cls}" style="grid-row:{lane_row[ln["id"]]}"></div>')
        parts.append(f'<div class="lname" style="grid-row:{lane_row[ln["id"]]}"><b>{e(ln["name"])}</b>'
                     f'<span>{e(ln.get("note", "")).replace(chr(10), "<br>")}</span></div>')
    for st in steps:
        tag = {"free": '<span class="tag free">FREE</span>', "paid": '<span class="tag paid">PAID</span>'}.get(st.get("cost") or "", "")
        cls = "box key" if st.get("highlight") else "box"
        parts.append(f'<div class="{cls}" id="{e(st["id"])}" style="grid-row:{lane_row[st["lane"]]};grid-column:{st["col"] + 1}">'
                     f'<div class="n">{e(str(st["n"]))}</div><h3>{e(st["title"])}</h3><p>{e(st["text"])}</p>{tag}</div>')
    parts.append('</div>')
    parts.append(f'<svg id="s"><defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">'
                 f'<path d="M0,0 L10,5 L0,10 z" fill="{THEME["violet"]}"/></marker></defs></svg>')
    parts.append(f'<script>{JS % dict(THEME, arrows=json.dumps(spec.get("arrows", [])))}</script></body></html>')
    return "".join(parts)


def render(html_path, png_path):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    o = Options()
    for a in ("--headless=new", "--window-size=1600,1400", "--force-device-scale-factor=2", "--hide-scrollbars"):
        o.add_argument(a)
    d = webdriver.Chrome(options=o)
    try:
        d.get("file://" + os.path.abspath(html_path))
        for _ in range(40):
            if d.execute_script("return document.body.getAttribute('data-ready')"):
                break
            time.sleep(0.3)
        h = d.execute_script("return document.body.scrollHeight")
        d.set_window_size(1600, h + 200)
        time.sleep(0.6)
        d.find_element(By.TAG_NAME, "body").screenshot(png_path)
    finally:
        d.quit()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1]))
    ids = {st["id"] for st in spec["steps"]}
    lanes = {ln["id"] for ln in spec["lanes"]}
    bad = [a for a in spec.get("arrows", []) if a["from"] not in ids or a["to"] not in ids]
    bad += [st for st in spec["steps"] if st["lane"] not in lanes]
    if bad:
        sys.exit(f"Unknown step or lane ids: {bad}")
    png = sys.argv[2]
    html_path = os.path.splitext(png)[0] + ".html"
    open(html_path, "w").write(build_html(spec))
    if "--html-only" in sys.argv:
        print(html_path)
        return
    render(html_path, png)
    print(png)


if __name__ == "__main__":
    main()
