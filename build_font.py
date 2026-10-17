#!/usr/bin/env python3
"""
Alien Glyphs — build_font.py
Draws every glyph from angular polyline strokes (45/90 deg language, chevrons,
open corners, segmented construction like the reference) on a 6 x 10 grid,
expands strokes to filled outlines, and builds TTF + WOFF2 + specimen + preview.
Grid: x 0..6 (left->right), y 0..10 (baseline->cap height). Lowercase mostly y 0..7.
Transform: X = 60 + x*80, Y = y*70  (cap 700, x-height 490, descender to -210)
Stroke width: 64 units on 1000 UPM.
"""
import math, os
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

OUT = os.path.dirname(os.path.abspath(__file__))
STROKE = 64
SX, SY, OX = 80, 70, 60

def D(cx, cy, r=0.42):  # filled diamond (dot)
    return [(cx, cy+r), (cx+r, cy), (cx, cy-r), (cx-r, cy)]

# Each entry: char -> (advance_in_grid_units, [polylines], [filled polygons])
# Polyline = list of (x,y). Closed shapes repeat first point at end.
G = {}
def g(ch, strokes, polys=None, adv=6):
    G[ch] = (adv, strokes, polys or [])

# ---------- UPPERCASE ----------
g('A', [[(0,0),(3,10),(6,0)], [(1.3,3.6),(4.7,3.6)]])
g('B', [[(0,0),(0,10),(4.3,10),(6,8),(4.3,5.2),(0,5.2)], [(4.3,5.2),(6,2.6),(4.3,0),(0,0)]])
g('C', [[(6,8),(4.5,10),(1.5,10),(0,8),(0,2),(1.5,0),(4.5,0),(6,2)]])
g('D', [[(0,0),(0,10),(3.4,10),(6,7.2),(6,2.8),(3.4,0),(0,0)]])
g('E', [[(6,10),(0,10),(0,0),(6,0)], [(0,5.1),(4.6,5.1)]])
g('F', [[(6,10),(0,10),(0,0)], [(0,5.1),(4.4,5.1)]])
g('G', [[(6,8),(4.5,10),(1.5,10),(0,8),(0,2),(1.5,0),(4.5,0),(6,2),(6,4.2),(3.4,4.2)]])
g('H', [[(0,0),(0,10)],[(6,0),(6,10)],[(0,5.1),(6,5.1)]])
g('I', [[(1,10),(5,10)],[(3,10),(3,0)],[(1,0),(5,0)]], adv=5)
g('J', [[(5,10),(5,1.8),(3.8,0),(1.2,0),(0,1.8)],[(2.5,10),(6,10)]], adv=5.5)
g('K', [[(0,0),(0,10)],[(5.8,10),(0.6,4.6)],[(1.6,5.6),(6,0)]])
g('L', [[(0,10),(0,0),(6,0)]])
g('M', [[(0,0),(0,10),(3,6.8),(6,10),(6,0)]])
g('N', [[(0,0),(0,10),(6,0),(6,10)]])
g('O', [[(1.5,0),(4.5,0),(6,2),(6,8),(4.5,10),(1.5,10),(0,8),(0,2),(1.5,0)]])
g('P', [[(0,0),(0,10),(4.3,10),(6,8.2),(4.3,5.8),(0,5.8)]])
g('Q', [[(1.5,0),(4.5,0),(6,2),(6,8),(4.5,10),(1.5,10),(0,8),(0,2),(1.5,0)],[(3.2,2.8),(6.2,-0.4)]])
g('R', [[(0,0),(0,10),(4.3,10),(6,8.2),(4.3,5.8),(0,5.8)],[(3.2,5.8),(6,0)]])
g('S', [[(6,8.6),(4.8,10),(1.2,10),(0,8.4),(0,6.2),(1.2,5.1),(4.8,5.1),(6,3.8),(6,1.6),(4.8,0),(0,0)]])
g('T', [[(0,10),(6,10)],[(3,10),(3,0)]])
g('U', [[(0,10),(0,2),(1.5,0),(4.5,0),(6,2),(6,10)]])
g('V', [[(0,10),(3,0),(6,10)]])
g('W', [[(0,10),(1.4,0),(3,6.2),(4.6,0),(6,10)]])
g('X', [[(0,10),(6,0)],[(0,0),(6,10)]])
g('Y', [[(0,10),(3,5),(6,10)],[(3,5),(3,0)]])
g('Z', [[(0,10),(6,10),(0,0),(6,0)]])
# ---------- lowercase (distinct variant forms, x-height 7) ----------
g('a', [[(5,0),(5,7),(1.2,7),(0,5.2),(0,1.8),(1.2,0),(5,0)],[(0,3.4),(3.6,3.4)]], adv=5.5)
g('b', [[(0,10),(0,0)],[(0,1.6),(1.4,0),(4.2,0),(5.4,1.8),(5.4,5),(4.2,7),(0,7)]], adv=5.8)
g('c', [[(5.4,5.4),(4.2,7),(1.4,7),(0,5.4),(0,1.6),(1.4,0),(4.2,0),(5.4,1.6)]], adv=5.8)
g('d', [[(5.4,10),(5.4,0)],[(5.4,1.6),(4.2,0),(1.4,0),(0,1.8),(0,5),(1.4,7),(4.2,7),(5.4,5.4)]], adv=5.8)
g('e', [[(0,3.6),(5.4,3.6),(5.4,5.4),(4.2,7),(1.4,7),(0,5.4),(0,1.6),(1.4,0),(4.2,0),(5.4,1.4)]], adv=5.8)
g('f', [[(4.6,8.8),(3.4,10),(1.6,10),(1.4,0)],[(0,5.4),(4.2,5.4)]], adv=4.6)
g('g', [[(5.4,7),(5.4,-1.2),(4.2,-2.6),(1.4,-2.6),(0,-1.4)],[(5.4,5.4),(4.2,7),(1.4,7),(0,5),(0,1.8),(1.4,0),(4.2,0),(5.4,1.6)]], adv=5.8)
g('h', [[(0,10),(0,0)],[(0,3.8),(1.6,7),(4.2,7),(5.4,5.2),(5.4,0)]], adv=5.8)
g('i', [[(2.6,7),(2.6,0)],[(1,0),(4.2,0)]], polys=[D(2.6,8.8)], adv=4.6)
g('j', [[(3.4,7),(3.4,-1.4),(2.2,-2.6),(0.4,-2.6)]], polys=[D(3.4,8.8)], adv=4.4)
g('k', [[(0,10),(0,0)],[(5,7),(0.8,3.4)],[(1.8,4.4),(5.4,0)]], adv=5.6)
g('l', [[(2.4,10),(2.4,0)],[(1,0),(4,0)]], adv=4.4)
g('m', [[(0,0),(0,7)],[(0,5.2),(1.8,7),(3,5.4),(3,0)],[(3,5.2),(4.6,7),(6,5.4),(6,0)]], adv=6.4)
g('n', [[(0,0),(0,7)],[(0,4.6),(1.8,7),(4.6,7),(5.6,5),(5.6,0)]], adv=6)
g('o', [[(1.4,0),(4.2,0),(5.6,1.6),(5.6,5.4),(4.2,7),(1.4,7),(0,5.4),(0,1.6),(1.4,0)]], adv=6)
g('p', [[(0,-3),(0,7),(4.2,7),(5.4,5),(4.2,2.2),(0,2.2)]], adv=5.8)
g('q', [[(5.4,-3),(5.4,7),(1.4,7),(0,5.2),(0,1.8),(1.4,0),(4.2,0),(5.4,1.4)],[(5.4,-1),(6.4,-3)]], adv=5.8)
g('r', [[(0,0),(0,7)],[(0,4.8),(2,7),(5.2,7),(5.6,5.6)]], adv=5.4)
g('s', [[(5.4,5.8),(4.4,7),(1.2,7),(0,5.8),(0,4.4),(1.2,3.6),(4.4,3.6),(5.4,2.4),(5.4,1),(4.2,0),(0,0)]], adv=5.8)
g('t', [[(2.6,9.4),(2.6,1.4),(3.8,0),(5.4,0)],[(0.4,6.4),(5,6.4)]], adv=5.2)
g('u', [[(0,7),(0,1.6),(1.4,0),(4.2,0),(5.4,1.6),(5.4,7)],[(5.4,1.2),(5.4,0)]], adv=5.8)
g('v', [[(0,7),(2.8,0),(5.6,7)]], adv=6)
g('w', [[(0,7),(1.3,0),(2.8,4.6),(4.3,0),(5.6,7)]], adv=6)
g('x', [[(0,7),(5.4,0)],[(0,0),(5.4,7)]], adv=5.8)
g('y', [[(0,7),(2.7,3.4),(5.4,7)],[(2.7,3.4),(2.7,-1.4),(1.6,-2.6),(0,-2.6)]], adv=5.8)
g('z', [[(0,7),(5.4,7),(0,0),(5.4,0)]], adv=5.8)
# ---------- digits ----------
g('0', [[(1.5,0),(4.5,0),(6,2),(6,8),(4.5,10),(1.5,10),(0,8),(0,2),(1.5,0)],[(1.2,1.2),(4.8,8.8)]])
g('1', [[(1.2,7.6),(3.6,10),(3.6,0)],[(1,0),(5.6,0)]], adv=5.6)
g('2', [[(0,8.2),(1.4,10),(4.8,10),(6,8.2),(0,0),(6,0)]])
g('3', [[(0,8.6),(1.4,10),(4.6,10),(6,8.4),(4.2,5.4),(1.6,5.4)],[(4.2,5.4),(6,3),(4.6,0),(0,0)]])
g('4', [[(4.2,0),(4.2,10),(0,3.2),(6,3.2)]])
g('5', [[(5.8,10),(0.6,10),(0,5.6),(4.4,5.6),(6,4),(4.8,0),(0,0)]])
g('6', [[(5.4,8.8),(4,10),(1.4,10),(0,8.2),(0,1.8),(1.4,0),(4.4,0),(6,1.8),(6,4.6),(4.4,6.4),(0,5)]])
g('7', [[(0,10),(6,10),(2.2,0)]])
g('8', [[(1.6,5.4),(0,7),(1.4,10),(4.6,10),(6,7),(4.4,5.4),(1.6,5.4)],[(4.4,5.4),(6,2.6),(4.6,0),(1.4,0),(0,2.6),(1.6,5.4)]])
g('9', [[(0.6,1.2),(2,0),(4.6,0),(6,1.8),(6,8.2),(4.6,10),(1.6,10),(0,8.2),(0,5.4),(1.6,3.6),(6,5)]])
# ---------- punctuation / symbols ----------
g(' ', [], adv=3)
g('!', [[(2.6,10),(2.6,3.2)]], polys=[D(2.6,1)], adv=4.6)
g('"', [[(1.4,10),(0.8,6.8)],[(4.4,10),(3.8,6.8)]], adv=5.6)
g('#', [[(1.8,0),(2.4,10)],[(4.6,0),(5.2,10)],[(0,3.4),(6.2,4.2)],[(0,6.4),(6.2,7.2)]], adv=6.4)
g('$', [[(5.6,8.6),(4.6,10),(1.4,10),(0,8.2),(0,6),(1.4,5),(4.6,5),(5.6,3.6),(5.6,1.4),(4.4,0),(0.4,0)],[(3,10.8),(3,-0.8)]])
g('%', [[(0.6,0),(5.8,10)]], polys=[D(0.9,8.6,0.65), D(5.3,1.4,0.65)])
g('&', [[(5.6,0),(2.4,4.2),(0.6,6.8),(1.2,9.4),(3.6,10),(5.2,8.4),(2.6,5),(1.2,2.2),(2.2,0),(4,0),(5.6,0)]])
g("'", [[(2.6,10),(2,6.8)]], adv=4)
g('(', [[(4.6,10),(1.6,7),(1.6,3),(4.6,0)]], adv=5)
g(')', [[(1.4,10),(4.4,7),(4.4,3),(1.4,0)]], adv=5)
g('*', [[(3,9),(3,3)],[(0.6,7.6),(5.4,4.4)],[(5.4,7.6),(0.6,4.4)]], adv=6)
g('+', [[(3,8),(3,2)],[(0.4,5),(5.6,5)]], adv=6)
g(',', [[(2.8,1.8),(2,-1)]], polys=[D(2.8,2.6,0.42)], adv=4.4)
g('-', [[(0.6,5),(5,5)]], adv=5.6)
g('.', [], polys=[D(2.4,0.8)], adv=4.4)
g('/', [[(0.6,-0.4),(5.4,10.4)]], adv=5.6)
g(':', [], polys=[D(2.6,7.6), D(2.6,1.6)], adv=4.6)
g(';', [[(2.8,1.6),(2,-1.2)]], polys=[D(2.8,7.4), D(2.9,2.4,0.42)], adv=4.6)
g('<', [[(5.4,8.6),(0.6,5),(5.4,1.4)]], adv=6)
g('=', [[(0.4,6.8),(5.6,6.8)],[(0.4,3.2),(5.6,3.2)]], adv=6)
g('>', [[(0.6,8.6),(5.4,5),(0.6,1.4)]], adv=6)
g('?', [[(0.8,8.4),(2,10),(4.8,10),(6,8.2),(6,6.4),(3,4),(3,2.8)]], polys=[D(3,0.9)], adv=6.2)
g('@', [[(5.2,2.6),(5.2,6.4),(4,7.4),(2,7.4),(0.8,6.2),(0.8,3.4),(2,2.2),(4,2.2),(5.2,3.4)],[(5.2,6.4),(6,8),(4.8,10),(1.6,10),(0,7.8),(0,2.2),(1.6,0),(4.8,0),(6,1.2)]], adv=6.6)
g('[', [[(4.8,10),(1.6,10),(1.6,0),(4.8,0)]], adv=5)
g('\\', [[(5.4,-0.4),(0.6,10.4)]], adv=5.6)
g(']', [[(1.2,10),(4.4,10),(4.4,0),(1.2,0)]], adv=5)
g('^', [[(1,6.4),(3,9.4),(5,6.4)]], adv=6)
g('_', [[(0,-1.2),(6,-1.2)]], adv=6.2)
g('`', [[(1.8,10),(3,7)]], adv=4)
g('{', [[(4.8,10),(2.6,10),(2.6,6.6),(1,5),(2.6,3.4),(2.6,0),(4.8,0)]], adv=5.4)
g('|', [[(2.8,10),(2.8,0)]], adv=4.4)
g('}', [[(1.2,10),(3.4,10),(3.4,6.6),(5,5),(3.4,3.4),(3.4,0),(1.2,0)]], adv=5.4)
g('~', [[(0,5.6),(1.8,7.8),(3.4,4.6),(5,7),(6,5.8)]], adv=6.2)
# extras beyond ASCII
g('\u2013', [[(0.6,5),(4.6,5)]], adv=5.2)   # en dash
g('\u2014', [[(0.2,5),(6.4,5)]], adv=7)     # em dash
g('\u2022', [], polys=[D(3,5,0.6)], adv=5)  # bullet
g('\u2026', [], polys=[D(1,0.8),D(3.2,0.8),D(5.4,0.8)], adv=6.4)  # ellipsis

GLYPH_NAMES = {' ':'space','!':'exclam','"':'quotedbl','#':'numbersign','$':'dollar','%':'percent','&':'ampersand',"'":'quotesingle','(':'parenleft',')':'parenright','*':'asterisk','+':'plus',',':'comma','-':'hyphen','.':'period','/':'slash',':':'colon',';':'semicolon','<':'less','=':'equal','>':'greater','?':'question','@':'at','[':'bracketleft','\\':'backslash',']':'bracketright','^':'asciicircum','_':'underscore','`':'grave','{':'braceleft','|':'bar','}':'braceright','~':'asciitilde','\u2013':'endash','\u2014':'emdash','\u2022':'bullet','\u2026':'ellipsis'}
def glyph_name(ch):
    if ch in GLYPH_NAMES: return GLYPH_NAMES[ch]
    if ch.isupper(): return ch
    if ch.islower(): return ch
    if ch.isdigit(): return ['zero','one','two','three','four','five','six','seven','eight','nine'][int(ch)]
    return f'uni{ord(ch):04X}'

def tx(p): return (OX + p[0]*SX, p[1]*SY)
def stroke_contours(strokes):
    contours, h = [], STROKE/2
    for line in strokes:
        pts = [tx(p) for p in line]
        for a,b in zip(pts, pts[1:]):
            dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx,dy) or 1
            px, py = -dy/L*h, dx/L*h
            contours.append([(a[0]+px,a[1]+py),(b[0]+px,b[1]+py),(b[0]-px,b[1]-py),(a[0]-px,a[1]-py)])
        for (x,y) in pts:  # square joint filler
            contours.append([(x-h,y-h),(x-h,y+h),(x+h,y+h),(x+h,y-h)])
    return contours

def build():
    chars = [chr(c) for c in range(0x20,0x7F)] + ['\u2013','\u2014','\u2022','\u2026']
    missing = [c for c in chars if c not in G]
    assert not missing, f"missing glyph defs: {missing!r}"
    order = ['.notdef'] + [glyph_name(c) for c in chars]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(c): glyph_name(c) for c in chars})
    metrics = {glyph_name(c): (int((G[c][0]*SX)+2*OX), 0) for c in chars}
    metrics['.notdef'] = (600,0); metrics['space'] = (int(3*SX+2*OX),0)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=800, descent=-300)
    fb.setupNameTable({
        'familyName':'Alien Glyphs','styleName':'Regular','uniqueFontIdentifier':'Alien Glyphs Regular v1.0',
        'fullName':'Alien Glyphs Regular','psName':'AlienGlyphs-Regular','version':'Version 1.0',
        'copyright':'Copyright 2026 Vincent. Alien Glyphs — angular sci-fi display font inspired by a mint-green segmented reference.',
        'manufacturer':'Alien Glyphs','designer':'Alien Glyphs (for Vincent)',
        'description':'Thin angular segmented display font: 45/90-degree strokes, chevrons, open corners and asymmetric cuts. Covers all printable ASCII plus en/em dash, bullet and ellipsis.',
        'licenseDescription':'User to choose final license; SIL Open Font License 1.1 suggested. See README.md.',
        'licenseInfoURL':'https://scripts.sil.org/OFL',
    })
    try:
        fb.setupOS2(sTypoAscender=800, sTypoDescender=-300, usWinAscent=850, usWinDescent=350, fsSelection=0b1000000)
    except Exception as e:
        print('OS2 warn', e); fb.setupOS2()
    fb.setupPost()
    fb.font['head'].unitsPerEm = 1000
    glyphs = {}
    def draw(name, strokes, polys):
        pen = TTGlyphPen(None)
        for cont in stroke_contours(strokes) + [[tx(p) for p in poly] for poly in polys]:
            pen.moveTo(cont[0])
            for p in cont[1:]: pen.lineTo(p)
            pen.closePath()
        glyphs[name] = pen.glyph()
    draw('.notdef', [[(0,0),(6,0),(6,10),(0,10),(0,0)],[(0,10),(6,0)],[(0,0),(6,10)]], [])
    for c in chars:
        adv, strokes, polys = G[c]
        draw(glyph_name(c), strokes, polys)
    fb.setupGlyf(glyphs)
    ttf = os.path.join(OUT,'AlienGlyphs-Regular.ttf')
    fb.save(ttf)
    f = TTFont(ttf); f.flavor='woff2'; woff = os.path.join(OUT,'AlienGlyphs-Regular.woff2'); f.save(woff); f.close()
    print('built', ttf, os.path.getsize(ttf), woff, os.path.getsize(woff), 'glyphs', len(chars))
    return chars

README = """# Alien Glyphs

A thin, angular, segmented sci-fi display font for Vincent — inspired by the
mint-green-on-black reference: sharp 45°/90° strokes, chevrons, open corners,
asymmetric cuts, no curves. The font itself is monochrome; use #7CFFB2 on black
to recreate the reference glow.

## Files
- `AlienGlyphs-Regular.ttf` — installable TrueType font
- `AlienGlyphs-Regular.woff2` — web font (used by preview.html)
- `build_font.py` — data-driven source; edit glyph polylines and re-run `python3 build_font.py`
- `specimen.png` — full specimen on black with mint-green glow
- `preview.html` — open in a browser, type in the box, see your text in Alien Glyphs

## Character set (99 glyphs)
All printable ASCII 0x20–0x7E (95, incl. space) plus – — • …

Uppercase: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Lowercase: a b c d e f g h i j k l m n o p q r s t u v w x y z (distinct small/variant forms, x-height)
Digits: 0 1 2 3 4 5 6 7 8 9
Symbols: . , ! ? : ; ' \" ` - – — _ ( ) [ ] { } / \\ | @ # $ % ^ & * + = < > ~ • …

## Install
- **Windows:** right-click `AlienGlyphs-Regular.ttf` → Install, or copy to `C:\\Windows\\Fonts`.
- **macOS:** double-click the TTF → Install Font (Font Book), or copy to `~/Library/Fonts`.
- **Linux / NixOS:** copy to `~/.local/share/fonts/` then `fc-cache -f`. NixOS declarative:
  add the TTF via `fonts.packages` with a derivation, or imperatively use the user fonts dir above.
- **Web:** keep the WOFF2 next to `preview.html`; `@font-face` is already wired up.

## Design notes
- 1000 UPM, cap height 700, x-height 490, stroke 64 units, only straight segments.
- Each glyph is defined in `build_font.py` as polylines on a 6×10 grid (`G` dict),
  expanded to filled outlines — tweak points, re-run, regenerate everything.
- Family: Alien Glyphs · Style: Regular · Version 1.0

## License
Vincent's to choose. Suggested: SIL Open Font License 1.1 (OFL) if sharing,
or keep all rights reserved for personal use — replace this note when decided.
"""

HTML = """<!doctype html><meta charset="utf-8"><title>Alien Glyphs — Preview</title>
<style>
@font-face{font-family:'Alien Glyphs';src:url('AlienGlyphs-Regular.woff2') format('woff2')}
body{background:#000;color:#7CFFB2;font-family:sans-serif;margin:40px}
h1,.out{font-family:'Alien Glyphs',monospace;text-shadow:0 0 6px #7CFFB2,0 0 18px #2eff8b88,0 0 42px #2eff8b44}
h1{font-size:64px;letter-spacing:.08em}
input{width:100%;box-sizing:border-box;background:#061a0e;color:#d8ffe9;border:1px solid #7CFFB2;padding:14px;font-size:20px}
.out{font-size:56px;line-height:1.5;white-space:pre-wrap;word-break:break-word;margin-top:24px;min-height:200px}
.small{font-family:'Alien Glyphs';font-size:28px;line-height:1.6}
</style>
<h1>ALIEN GLYPHS</h1>
<input id="t" value="HELLO WORLD 0123456789" autocomplete="off">
<div class="out" id="o"></div>
<p class="small">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 !?@#$%&amp;*+-=&lt;&gt;</p>
<script>const t=document.getElementById('t'),o=document.getElementById('o');const f=()=>o.textContent=t.value; t.addEventListener('input',f); f();</script>
"""

def specimen(chars):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    W,H = 2400, 1900
    alien = lambda s: ImageFont.truetype(os.path.join(OUT,'AlienGlyphs-Regular.ttf'), s)
    sans = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
    img = Image.new('RGB',(W,H),(0,0,0)); glow = Image.new('RGB',(W,H),(0,0,0))
    gd = ImageDraw.Draw(glow); d = ImageDraw.Draw(img)
    MINT=(124,255,178); DIM=(90,140,110)
    def text(draw, xy, s, font, fill): draw.text(xy, s, font=font, fill=fill)
    # glow layer: titles + samples
    lines = [(90,60,'ALIEN GLYPHS',alien(150)), (90,240,'HELLO WORLD 0123456789',alien(82)),
             (90,350,'THE QUICK BROWN FOX JUMPS OVER',alien(64)), (90,435,'THE LAZY DOG 0123456789 !?',alien(64))]
    for x,y,s,f in lines: text(gd,(x,y),s,f,MINT)
    # grid of every printable glyph with label
    gx, gy, cw, chh = 90, 580, 138, 148
    cols = 16
    printable = [chr(c) for c in range(0x21,0x7F)] + ['\u2013','\u2014','\u2022','\u2026']
    for i,c in enumerate(printable):
        x = gx + (i%cols)*cw; y = gy + (i//cols)*chh
        gd.text((x+18,y), c, font=alien(72), fill=MINT)
        d.text((x+22,y+92), ('U+%04X'%ord(c)), font=sans(17), fill=DIM)
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    img = Image.blend(img, Image.blend(img, glow, 0.9), 0.85)
    # sharp pass on top
    d = ImageDraw.Draw(img)
    for x,y,s,f in lines: text(d,(x,y),s,f,MINT)
    for i,c in enumerate(printable):
        x = gx + (i%cols)*cw; y = gy + (i//cols)*chh
        d.text((x+18,y), c, font=alien(72), fill=MINT)
        d.text((x+22,y+92), ('U+%04X'%ord(c)), font=sans(17), fill=DIM)
    d.text((90, gy+((len(printable)+cols-1)//cols)*chh+30), 'AaBbCc XxYyZz  0123456789  &@#%*+=<>  Alien Glyphs Regular', font=alien(52), fill=MINT)
    img.save(os.path.join(OUT,'specimen.png'))
    print('specimen', img.size)

if __name__ == '__main__':
    chars = build()
    open(os.path.join(OUT,'preview.html'),'w').write(HTML)
    open(os.path.join(OUT,'README.md'),'w').write(README)
    specimen(chars)
