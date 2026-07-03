#!/usr/bin/env python3
"""EggShell Organic — packaging artwork generator.

Emits:
  eggshell-front-flat.svg  (2400x1000)  - print-style front face
  eggshell-box-3d.svg      (2048x2048)  - axonometric box mockup (feed to image-to-3D)
"""
import random, math, os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
KRAFT      = "#D9BC8F"
KRAFT_DK   = "#C9A876"
GREEN      = "#1E4023"
GREEN_DK   = "#16341C"
CREAM      = "#F6EDDA"
GOLD       = "#B8860B"
GOLD_LT    = "#D4A93C"
BROWN      = "#7A4A21"
EGG_A, EGG_B, EGG_C = "#B57B4A", "#C08A57", "#A96F42"

SERIF = "Baskerville, Georgia, serif"
SANS  = "'Avenir Next', 'Helvetica Neue', sans-serif"

# ---------------------------------------------------------------- helpers
def speckles(w, h, n, seed):
    random.seed(seed)
    out = []
    for _ in range(n):
        x, y = random.uniform(0, w), random.uniform(0, h)
        r = random.uniform(0.8, 2.6)
        o = random.uniform(0.04, 0.11)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{BROWN}" opacity="{o:.2f}"/>')
    return "".join(out)

def grass_tufts(x0, x1, y, n, seed, color=GREEN, op=0.9):
    random.seed(seed)
    out = []
    for _ in range(n):
        x = random.uniform(x0, x1)
        hgt = random.uniform(10, 26)
        lean = random.uniform(-6, 6)
        out.append(f'<path d="M{x:.0f},{y} q{lean:.0f},-{hgt*0.7:.0f} {lean*1.4:.0f},-{hgt:.0f}" stroke="{color}" stroke-width="2.2" fill="none" opacity="{op}"/>')
    return "".join(out)

# ---------------------------------------------------------------- logo (200x250 box)
def logo(scale=1.0, stroke=GREEN, leaf=GREEN, accent=GOLD):
    return f'''
    <g transform="scale({scale})">
      <!-- egg -->
      <path d="M100,8 C140,8 166,64 166,118 C166,168 138,198 100,198 C62,198 34,168 34,118 C34,64 60,8 100,8 Z"
            fill="none" stroke="{stroke}" stroke-width="9"/>
      <path d="M100,30 C130,30 150,74 150,116 C150,156 128,180 100,180 C72,180 50,156 50,116 C50,74 70,30 100,30 Z"
            fill="{stroke}"/>
      <path d="M78,60 C70,80 66,100 68,120" stroke="{CREAM}" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.85"/>
      <!-- leaves at base -->
      <path d="M100,196 C64,210 34,206 18,182 C48,172 82,176 100,196 Z" fill="{leaf}" stroke="{accent}" stroke-width="3"/>
      <path d="M100,196 C136,210 166,206 182,182 C152,172 118,176 100,196 Z" fill="{leaf}" stroke="{accent}" stroke-width="3"/>
      <path d="M100,244 C84,224 84,206 100,190 C116,206 116,224 100,244 Z" fill="{leaf}" stroke="{accent}" stroke-width="3"/>
      <path d="M100,238 L100,196 M100,214 L88,204 M100,214 L112,204" stroke="{accent}" stroke-width="2.5" fill="none"/>
    </g>'''

# ---------------------------------------------------------------- hen (engraving-style, 440x470 box, faces right)
HEN = f'''
  <g stroke="{GREEN_DK}" stroke-linejoin="round" stroke-linecap="round">
    <!-- tail plumes -->
    <path d="M120,180 C50,90 40,60 70,28 C96,72 116,110 148,150 Z" fill="{GREEN}" stroke-width="4"/>
    <path d="M132,196 C60,140 34,104 44,62 C84,102 122,140 158,168 Z" fill="{GREEN}" stroke-width="4"/>
    <path d="M146,210 C74,178 46,150 44,110 C94,142 136,168 172,188 Z" fill="{GREEN}" stroke-width="4"/>
    <!-- body -->
    <path d="M118,240 C118,170 180,128 258,128 C302,128 330,116 344,92
             C356,102 356,118 348,130 C368,128 382,136 388,152
             C376,158 366,160 356,162 C388,196 400,238 388,282
             C374,332 322,368 258,368 C182,368 118,318 118,240 Z"
          fill="{GREEN}" stroke-width="5"/>
    <!-- comb -->
    <g transform="translate(8,12)">
      <path d="M304,88 C300,66 308,52 322,44 C324,58 332,64 340,60 C338,74 348,80 358,76 C352,92 344,98 332,100 Z"
            fill="#8C3B2E" stroke="#6E2C22" stroke-width="3"/>
    </g>
    <!-- wattle -->
    <path d="M352,142 C362,152 364,166 356,176 C346,170 342,156 346,144 Z" fill="#8C3B2E" stroke="#6E2C22" stroke-width="3"/>
    <!-- beak -->
    <path d="M382,140 L412,150 L384,162 Z" fill="{GOLD_LT}" stroke="{BROWN}" stroke-width="3"/>
    <!-- eye -->
    <circle cx="344" cy="118" r="7" fill="{CREAM}"/>
    <circle cx="346" cy="118" r="3.4" fill="{GREEN_DK}"/>
    <!-- wing -->
    <path d="M170,220 C176,182 214,160 262,164 C288,166 302,182 300,204 C298,238 258,266 210,264 C182,262 166,246 170,220 Z"
          fill="none" stroke="{CREAM}" stroke-width="4.5" opacity="0.9"/>
    <path d="M188,236 C210,244 246,242 272,224 M182,214 C206,224 244,222 276,202" stroke="{CREAM}" stroke-width="3" fill="none" opacity="0.75"/>
    <!-- breast feather ticks -->
    <path d="M300,250 q10,10 4,22 M318,222 q10,10 4,22 M292,286 q10,10 4,22 M328,258 q8,10 3,20" stroke="{CREAM}" stroke-width="3" fill="none" opacity="0.6"/>
    <!-- legs -->
    <path d="M218,366 L214,430 M214,430 L192,452 M214,430 L216,456 M214,430 L234,450" stroke="{BROWN}" stroke-width="7" fill="none"/>
    <path d="M282,362 L286,430 M286,430 L264,452 M286,430 L288,456 M286,430 L306,450" stroke="{BROWN}" stroke-width="7" fill="none"/>
  </g>'''

# ---------------------------------------------------------------- farmhouse line art (420x330 box)
FARMHOUSE = f'''
  <g stroke="{GREEN}" stroke-width="4" fill="none" stroke-linejoin="round">
    <!-- barn -->
    <path d="M60,300 L60,170 L150,110 L240,170 L240,300 Z" fill="{KRAFT}"/>
    <path d="M42,178 L150,104 L258,178" stroke-width="6"/>
    <path d="M60,196 L240,196 M60,224 L240,224 M60,252 L240,252 M60,280 L240,280" stroke-width="2" opacity="0.5"/>
    <rect x="122" y="226" width="56" height="74" fill="{GREEN}" opacity="0.9"/>
    <path d="M122,226 L178,300 M178,226 L122,300" stroke="{KRAFT}" stroke-width="3"/>
    <circle cx="150" cy="166" r="16"/>
    <path d="M150,150 L150,182 M134,166 L166,166"/>
    <!-- silo -->
    <path d="M280,300 L280,150 C280,124 340,124 340,150 L340,300" fill="{KRAFT}"/>
    <path d="M280,150 C280,124 340,124 340,150" fill="none"/>
    <path d="M286,176 L334,176 M286,206 L334,206 M286,236 L334,236 M286,266 L334,266" stroke-width="2" opacity="0.5"/>
    <!-- tree -->
    <path d="M392,300 L392,236" stroke-width="6"/>
    <circle cx="392" cy="208" r="34" fill="{KRAFT}"/>
    <path d="M368,196 q24,-18 48,0 M366,216 q26,16 52,0" stroke-width="2.5" opacity="0.6"/>
    <!-- ground -->
    <path d="M20,300 L420,300" stroke-width="5"/>
    <!-- birds -->
    <path d="M330,70 q8,-8 16,0 q8,-8 16,0 M380,92 q7,-7 14,0 q7,-7 14,0" stroke-width="3"/>
  </g>'''

# ---------------------------------------------------------------- basket of eggs (560x330 box)
def basket():
    eggs = []
    rows = [ (5, 92, 168), (4, 148, 118), (3, 208, 74) ]  # n, cy, startx-ish
    cols = [EGG_A, EGG_B, EGG_C]
    i = 0
    for n, cy, _ in [(5, 150, 0), (4, 105, 0), (3, 66, 0)]:
        total_w = n * 86
        x0 = (560 - total_w) / 2 + 43
        for k in range(n):
            cx = x0 + k * 86
            c = cols[i % 3]; i += 1
            eggs.append(f'''<g>
              <ellipse cx="{cx:.0f}" cy="{cy}" rx="40" ry="50" fill="{c}" stroke="{BROWN}" stroke-width="3"/>
              <ellipse cx="{cx-12:.0f}" cy="{cy-16}" rx="10" ry="16" fill="{CREAM}" opacity="0.45"/>
            </g>''')
    weave = []
    for yy in range(212, 300, 22):
        weave.append(f'<path d="M{60 + (yy-212)*0.9:.0f},{yy} Q280,{yy+16} {500 - (yy-212)*0.9:.0f},{yy}" stroke="{BROWN}" stroke-width="3" fill="none" opacity="0.7"/>')
    for xx in range(90, 480, 42):
        weave.append(f'<path d="M{xx},196 q6,60 {18 if xx < 280 else -2},96" stroke="{BROWN}" stroke-width="2.4" fill="none" opacity="0.45"/>')
    return f'''
    <g>
      {''.join(eggs)}
      <path d="M40,190 L88,306 C92,318 120,326 280,326 C440,326 468,318 472,306 L520,190 Z"
            fill="{KRAFT_DK}" stroke="{BROWN}" stroke-width="5"/>
      {''.join(weave)}
      <ellipse cx="280" cy="190" rx="242" ry="30" fill="none" stroke="{BROWN}" stroke-width="7"/>
      <ellipse cx="280" cy="190" rx="220" ry="22" fill="none" stroke="{BROWN}" stroke-width="3" opacity="0.6"/>
    </g>'''

# ---------------------------------------------------------------- roundel badge
def roundel(cx, cy, r, fill, ring, lines, fs, fill_txt=CREAM, sub_fs=None):
    tspans = ""
    n = len(lines)
    for i, ln in enumerate(lines):
        dy = (i - (n - 1) / 2) * (fs * 1.25)
        tspans += f'<text x="{cx}" y="{cy + dy + fs*0.35:.0f}" font-family="{SANS}" font-weight="700" font-size="{fs}" letter-spacing="1.5" fill="{fill_txt}" text-anchor="middle">{ln}</text>'
    return f'''
    <g>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>
      <circle cx="{cx}" cy="{cy}" r="{r-6}" fill="none" stroke="{ring}" stroke-width="2.5" stroke-dasharray="1 0"/>
      <circle cx="{cx}" cy="{cy}" r="{r-11}" fill="none" stroke="{ring}" stroke-width="1.2" opacity="0.7"/>
      {tspans}
    </g>'''

# ---------------------------------------------------------------- non-veg mark (FSSAI 2020: brown triangle in brown square)
def nonveg(x, y, s=64):
    return f'''
    <g transform="translate({x},{y})">
      <rect x="0" y="0" width="{s}" height="{s}" fill="{CREAM}" stroke="#6E3A1F" stroke-width="4"/>
      <path d="M{s/2},{s*0.2} L{s*0.82},{s*0.78} L{s*0.18},{s*0.78} Z" fill="#6E3A1F"/>
      <text x="{s/2}" y="{s + 26}" font-family="{SANS}" font-size="17" font-weight="600" fill="#6E3A1F" text-anchor="middle" letter-spacing="1">NON-VEG</text>
    </g>'''

# ---------------------------------------------------------------- sunburst (behind title)
def sunburst(cx, cy, r0, r1, n=24):
    rays = []
    for i in range(n):
        a = math.pi * (1 + i / (n - 1))  # top half
        x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        rays.append(f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{GOLD}" stroke-width="2.4" opacity="0.5"/>')
    return "".join(rays)

# ---------------------------------------------------------------- FRONT FACE 2400x1000
def front_face():
    return f'''
  <g>
    <defs>
      <linearGradient id="kraftg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#E2C79C"/><stop offset="0.55" stop-color="{KRAFT}"/><stop offset="1" stop-color="{KRAFT_DK}"/>
      </linearGradient>
    </defs>
    <rect width="2400" height="1000" fill="url(#kraftg)"/>
    {speckles(2400, 1000, 340, 7)}

    <!-- keylines -->
    <rect x="26" y="26" width="2348" height="948" fill="none" stroke="{GOLD}" stroke-width="3"/>
    <rect x="38" y="38" width="2324" height="924" fill="none" stroke="{GOLD}" stroke-width="1.4" opacity="0.8"/>

    <!-- sunburst behind brand -->
    {sunburst(1200, 490, 260, 430)}

    <!-- corner marks -->
    {nonveg(80, 80)}
    {roundel(2110, 160, 92, GREEN, GOLD_LT, ["HIGH", "PROTEIN"], 26)}
    {roundel(2262, 332, 84, BROWN, GOLD_LT, ["PREMIUM", "BROWN", "EGGS"], 20)}

    <!-- scene: hen left -->
    <g transform="translate(120,330)">{HEN}</g>
    <path d="M90,790 L600,790" stroke="{GREEN}" stroke-width="4" opacity="0.8"/>
    {grass_tufts(100, 600, 790, 42, 11)}
    <!-- fence left -->
    <g stroke="{GREEN}" stroke-width="4" opacity="0.75" fill="none">
      <path d="M96,700 L96,788 M156,700 L156,788 M216,700 L216,788 M70,722 L240,722 M70,756 L240,756"/>
    </g>

    <!-- scene: farm right -->
    <g transform="translate(1900,440)">{FARMHOUSE}</g>
    {grass_tufts(1910, 2320, 742, 34, 12)}

    <!-- brand block -->
    <g transform="translate(1145,50)">{logo(0.55)}</g>
    <text x="1200" y="316" font-family="{SERIF}" font-weight="700" font-size="118" fill="{GREEN}" text-anchor="middle">EggShell<tspan font-size="48" dy="-54">®</tspan></text>
    <text x="1194" y="404" font-family="{SANS}" font-weight="600" font-size="44" letter-spacing="12" fill="{GOLD}" text-anchor="middle">ORGANIC</text>

    <text x="1200" y="494" font-family="{SERIF}" font-weight="700" font-size="82" fill="{GREEN_DK}" text-anchor="middle" letter-spacing="2">Organic Country Eggs</text>

    <!-- tagline with rules -->
    <path d="M770,536 L985,536 M1415,536 L1630,536" stroke="{GOLD}" stroke-width="2.4"/>
    <path d="M1200,522 l10,14 l-10,14 l-10,-14 Z" fill="{GOLD}"/>
    <text x="1200" y="584" font-family="{SERIF}" font-style="italic" font-size="42" fill="{BROWN}" text-anchor="middle">Daily Protein, The Natural Way.</text>

    <!-- basket + count -->
    <g transform="translate(950,592) scale(0.88)">{basket()}</g>
    {roundel(1580, 762, 92, GREEN, GOLD_LT, ["12", "EGGS"], 34)}
    <text x="1580" y="642" font-family="{SANS}" font-weight="600" font-size="20" letter-spacing="3" fill="{GREEN}" text-anchor="middle">NET QUANTITY</text>

    <!-- lab-tested script note -->
    <text x="860" y="668" font-family="{SANS}" font-weight="600" font-size="24" fill="{GREEN}" text-anchor="end" letter-spacing="1">Lab Tested for</text>
    <text x="860" y="698" font-family="{SANS}" font-weight="600" font-size="24" fill="{GREEN}" text-anchor="end" letter-spacing="1">Antibiotic Residues</text>
    <circle cx="898" cy="676" r="16" fill="none" stroke="{GREEN}" stroke-width="3"/>
    <path d="M890,676 l6,7 l12,-14" stroke="{GREEN}" stroke-width="3.5" fill="none"/>

    <!-- bottom band -->
    <rect x="0" y="880" width="2400" height="120" fill="{GREEN}"/>
    <rect x="0" y="874" width="2400" height="3" fill="{GOLD_LT}"/>
    <text x="90" y="950" font-family="{SANS}" font-weight="600" font-size="30" letter-spacing="2" fill="{CREAM}">FARM FRESH &#8226; NATURALLY NUTRITIOUS</text>
    <text x="2310" y="950" font-family="{SANS}" font-weight="600" font-size="30" letter-spacing="2" fill="{CREAM}" text-anchor="end">ANTIBIOTIC-FREE COUNTRY BROWN EGGS</text>

    <!-- available-in pill -->
    <g>
      <rect x="930" y="908" width="540" height="64" rx="32" fill="{CREAM}" stroke="{GOLD}" stroke-width="3"/>
      <text x="1200" y="951" font-family="{SANS}" font-weight="700" font-size="30" letter-spacing="2" fill="{GREEN}" text-anchor="middle">AVAILABLE IN 6 / 12 / 30 EGGS</text>
    </g>
  </g>'''

# ---------------------------------------------------------------- TOP FACE 2400x760
def icon_roundel(cx, cy, label1, label2, glyph):
    return f'''
    <g>
      <circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{GREEN}" stroke-width="5"/>
      <circle cx="{cx}" cy="{cy}" r="64" fill="none" stroke="{GOLD}" stroke-width="1.6" opacity="0.8"/>
      {glyph}
      <text x="{cx}" y="{cy+118}" font-family="{SANS}" font-weight="600" font-size="27" fill="{GREEN}" text-anchor="middle">{label1}</text>
      <text x="{cx}" y="{cy+150}" font-family="{SANS}" font-weight="600" font-size="27" fill="{GREEN}" text-anchor="middle">{label2}</text>
    </g>'''

NUTRITION = [
    ("Energy", "156 kcal"), ("Protein", "13.19 g"), ("Total Fat", "11.09 g"),
    ("Saturated Fat", "3.31 g"), ("Carbohydrates", "0.60 g"), ("Total Sugar", "0 g"),
    ("Added Sugar", "0 g"), ("Cholesterol", "373.61 mg"),
]

def nutrition_table(x, y, w=620, rh=46, hh=56, fs=28, hfs=24):
    rows = ""
    for i, (k, v) in enumerate(NUTRITION):
        by = y + hh + i * rh
        band = f'<rect x="{x}" y="{by}" width="{w}" height="{rh}" fill="{CREAM}" opacity="{0.55 if i % 2 == 0 else 0.25}"/>'
        rows += f'''{band}
        <text x="{x+22}" y="{by+rh*0.7:.0f}" font-family="{SANS}" font-size="{fs}" font-weight="500" fill="{GREEN_DK}">{k}</text>
        <text x="{x+w-22}" y="{by+rh*0.7:.0f}" font-family="{SANS}" font-size="{fs}" font-weight="600" fill="{GREEN_DK}" text-anchor="end">{v}</text>'''
    hgt = hh + len(NUTRITION) * rh
    return f'''
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{hgt}" fill="none" stroke="{GREEN}" stroke-width="4"/>
      <rect x="{x}" y="{y}" width="{w}" height="{hh}" fill="{GREEN}"/>
      <text x="{x+w/2}" y="{y+hh*0.66:.0f}" font-family="{SANS}" font-weight="700" font-size="{hfs}" fill="{CREAM}" text-anchor="middle" letter-spacing="0.5">NUTRITION INFORMATION (Per 100 g)</text>
      {rows}
    </g>'''

def _leaf_glyph(cx, cy):
    return f'<path d="M{cx},{cy+30} C{cx-34},{cy+10} {cx-36},{cy-26} {cx-10},{cy-40} C{cx+8},{cy-14} {cx+10},{cy+12} {cx},{cy+30} Z" fill="{GREEN}"/><path d="M{cx},{cy+34} C{cx+2},{cy+6} {cx-2},{cy-18} {cx-8},{cy-34}" stroke="{CREAM}" stroke-width="2.5" fill="none"/>'

def _hen_glyph(cx, cy):
    return f'<g transform="translate({cx-33},{cy-36}) scale(0.155)">{HEN}</g>'

def _flask_glyph(cx, cy):
    return f'''<g stroke="{GREEN}" stroke-width="5" fill="none"><path d="M{cx-10},{cy-38} L{cx-10},{cy-8} L{cx-30},{cy+30} C{cx-34},{cy+40} {cx-28},{cy+44} {cx-20},{cy+44} L{cx+20},{cy+44} C{cx+28},{cy+44} {cx+34},{cy+40} {cx+30},{cy+30} L{cx+10},{cy-8} L{cx+10},{cy-38}"/><path d="M{cx-16},{cy-38} L{cx+16},{cy-38}"/><path d="M{cx-18},{cy+18} L{cx+18},{cy+18}" stroke-width="4"/><circle cx="{cx-4}" cy="{cy+30}" r="3.4" fill="{GREEN}"/><circle cx="{cx+9}" cy="{cy+33}" r="2.6" fill="{GREEN}"/></g>'''

def _globe_glyph(cx, cy):
    return f'''<g stroke="{GREEN}" stroke-width="4.5" fill="none"><circle cx="{cx}" cy="{cy}" r="36"/><path d="M{cx-36},{cy} L{cx+36},{cy} M{cx},{cy-36} C{cx+20},{cy-20} {cx+20},{cy+20} {cx},{cy+36} M{cx},{cy-36} C{cx-20},{cy-20} {cx-20},{cy+20} {cx},{cy+36}"/></g>'''

def top_face():
    icons = [
        (660, "Organic", "Farming", _leaf_glyph),
        (1020, "Free Range", "Hens", _hen_glyph),
        (1380, "No Antibiotics", "No Hormones", _flask_glyph),
        (1740, "Sustainable", "Practices", _globe_glyph),
    ]
    cy = 552
    icon_svg = "".join(icon_roundel(cx, cy, l1, l2, g(cx, cy)) for cx, l1, l2, g in icons)
    return f'''
  <g>
    <rect width="2400" height="760" fill="url(#kraftg)"/>
    {speckles(2400, 760, 220, 9)}
    <rect x="26" y="26" width="2348" height="708" fill="none" stroke="{GOLD}" stroke-width="3"/>
    <rect x="38" y="38" width="2324" height="684" fill="none" stroke="{GOLD}" stroke-width="1.4" opacity="0.8"/>

    <g transform="translate(1152,54)">{logo(0.48)}</g>
    <text x="1200" y="286" font-family="{SERIF}" font-weight="700" font-size="92" fill="{GREEN}" text-anchor="middle">EggShell<tspan font-size="38" dy="-42">®</tspan></text>
    <text x="1195" y="348" font-family="{SANS}" font-weight="600" font-size="36" letter-spacing="10" fill="{GOLD}" text-anchor="middle">ORGANIC</text>
    <path d="M820,392 L1050,392 M1350,392 L1580,392" stroke="{GOLD}" stroke-width="2.2"/>
    <path d="M1200,380 l9,12 l-9,12 l-9,-12 Z" fill="{GOLD}"/>
    <text x="1200" y="446" font-family="{SERIF}" font-style="italic" font-size="38" fill="{BROWN}" text-anchor="middle">Daily Protein, The Natural Way.</text>
    {icon_svg}
  </g>'''

# ---------------------------------------------------------------- SIDE FACE 760x1000
def side_face():
    return f'''
  <g>
    <rect width="760" height="1000" fill="{GREEN}"/>
    <rect x="22" y="22" width="716" height="956" fill="none" stroke="{GOLD_LT}" stroke-width="2.5" opacity="0.85"/>
    <g transform="translate(280,110)">{logo(1.0, CREAM, "#4E7A46", GOLD_LT)}</g>
    <text x="380" y="480" font-family="{SERIF}" font-weight="700" font-size="86" fill="{CREAM}" text-anchor="middle">EggShell</text>
    <text x="380" y="540" font-family="{SANS}" font-weight="600" font-size="36" letter-spacing="10" fill="{GOLD_LT}" text-anchor="middle">ORGANIC</text>
    <path d="M180,600 L580,600" stroke="{GOLD_LT}" stroke-width="2"/>
    <text x="380" y="668" font-family="{SERIF}" font-style="italic" font-size="35" fill="{CREAM}" text-anchor="middle">Daily Protein,</text>
    <text x="380" y="716" font-family="{SERIF}" font-style="italic" font-size="35" fill="{CREAM}" text-anchor="middle">The Natural Way.</text>
    <text x="380" y="830" font-family="{SANS}" font-weight="600" font-size="26" letter-spacing="2" fill="{CREAM}" text-anchor="middle" opacity="0.9">M R ENTERPRISE</text>
    <text x="380" y="866" font-family="{SANS}" font-size="23" letter-spacing="1.5" fill="{CREAM}" text-anchor="middle" opacity="0.75">(AGRO PRODUCTS)</text>
  </g>'''

# ---------------------------------------------------------------- barcode / QR placeholders
def barcode(x, y, w=340, h=110):
    random.seed(21)
    bars, bx = [], x
    while bx < x + w - 4:
        bw = random.choice([3, 3, 4, 6, 8])
        if random.random() > 0.42:
            bars.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{h}" fill="{GREEN_DK}"/>')
        bx += bw + random.choice([2, 3, 4])
    return f'''<g>{''.join(bars)}
      <text x="{x+w/2}" y="{y+h+30}" font-family="{SANS}" font-size="24" letter-spacing="4" fill="{GREEN_DK}" text-anchor="middle">8 906123 401234</text></g>'''

def qr(x, y, s=150):
    random.seed(33)
    m, cell = 21, s / 21
    px = []
    def finder(cx, cy):
        px.append(f'<rect x="{x+cx*cell:.1f}" y="{y+cy*cell:.1f}" width="{cell*7:.1f}" height="{cell*7:.1f}" fill="none" stroke="{GREEN_DK}" stroke-width="{cell:.1f}"/>')
        px.append(f'<rect x="{x+(cx+2)*cell:.1f}" y="{y+(cy+2)*cell:.1f}" width="{cell*3:.1f}" height="{cell*3:.1f}" fill="{GREEN_DK}"/>')
    finder(0, 0); finder(14, 0); finder(0, 14)
    for r in range(m):
        for c in range(m):
            if (r < 8 and c < 8) or (r < 8 and c > 12) or (r > 12 and c < 8):
                continue
            if random.random() > 0.52:
                px.append(f'<rect x="{x+c*cell:.1f}" y="{y+r*cell:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{GREEN_DK}"/>')
    return f'''<g>{''.join(px)}
      <text x="{x+s/2}" y="{y+s+32}" font-family="{SANS}" font-size="21" fill="{GREEN_DK}" text-anchor="middle">Scan for Farm Information</text></g>'''

# ---------------------------------------------------------------- declarations panel 2256x520
def declarations_panel():
    L = f'''
      <text x="40" y="66" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">INGREDIENTS</text>
      <text x="40" y="102" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">Organic Country Eggs (100%)</text>
      <text x="40" y="160" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">ALLERGEN DECLARATION</text>
      <text x="40" y="196" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">Contains Egg</text>
      <text x="40" y="254" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">STORAGE INSTRUCTIONS</text>
      <text x="40" y="290" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">Store in a cool and dry place.</text>
      <text x="40" y="324" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">Refrigerate for longer freshness.</text>
      <text x="40" y="382" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">BEST BEFORE</text>
      <text x="40" y="418" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">Best before 21 days from packing.</text>
      <text x="40" y="476" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">EGG SIZE: <tspan font-weight="500">LARGE</tspan>  &#8226;  COLOUR: <tspan font-weight="500">COUNTRY BROWN</tspan></text>'''
    M = f'''
      <text x="800" y="66" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">MANUFACTURER / MARKETER</text>
      <text x="800" y="102" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">M R Enterprise (Agro Products)</text>
      <text x="800" y="136" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">[Complete Address]</text>
      <text x="800" y="194" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">CUSTOMER CARE</text>
      <text x="800" y="230" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">[Phone]  &#8226;  [Email]</text>
      <g transform="translate(800,270)">
        <rect width="150" height="58" rx="8" fill="none" stroke="{GREEN}" stroke-width="3"/>
        <text x="75" y="39" font-family="{SANS}" font-weight="800" font-size="30" fill="{GREEN}" text-anchor="middle">fssai</text>
        <text x="176" y="30" font-family="{SANS}" font-size="25" fill="{GREEN_DK}">FSSAI Lic. No.:</text>
        <text x="176" y="60" font-family="{SANS}" font-size="25" fill="{GREEN_DK}">__________________</text>
      </g>
      <text x="800" y="398" font-family="{SANS}" font-weight="700" font-size="27" fill="{GREEN}" letter-spacing="1">NET QUANTITY</text>
      <text x="800" y="434" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">6 Eggs / 12 Eggs / 30 Eggs</text>
      <g transform="translate(800,452)">{''}</g>'''
    R = f'''
      <text x="1450" y="66" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">Batch No.: ____________</text>
      <text x="1450" y="112" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">Packed On: ____________</text>
      <text x="1450" y="158" font-family="{SANS}" font-size="26" fill="{GREEN_DK}">MRP (Incl. of all Taxes): &#8377; ______</text>
      {barcode(1450, 200)}
      {nonveg(1480, 390, 56)}
      {qr(1960, 120)}'''
    return f'''
  <g>
    <rect width="2256" height="520" fill="{CREAM}" stroke="{GREEN}" stroke-width="4"/>
    <rect x="10" y="10" width="2236" height="500" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity="0.7"/>
    <line x1="760" y1="36" x2="760" y2="484" stroke="{GOLD}" stroke-width="1.5" opacity="0.7"/>
    <line x1="1410" y1="36" x2="1410" y2="484" stroke="{GOLD}" stroke-width="1.5" opacity="0.7"/>
    {L}{M}{R}
  </g>'''

# ---------------------------------------------------------------- BACK FACE 2400x1000
def _block(x, y, title, lines, fs=25, lh=34):
    body = "".join(
        f'<text x="{x}" y="{y + 38 + i*lh}" font-family="{SANS}" font-size="{fs}" fill="{GREEN_DK}">{ln}</text>'
        for i, ln in enumerate(lines))
    return f'''
      <text x="{x}" y="{y}" font-family="{SANS}" font-weight="700" font-size="25" letter-spacing="1.5" fill="{GREEN}">{title}</text>
      <path d="M{x},{y+12} L{x+56},{y+12}" stroke="{GOLD}" stroke-width="2.4"/>
      {body}'''

def back_face():
    return f'''
  <g>
    <rect width="2400" height="1000" fill="url(#kraftg)"/>
    {speckles(2400, 1000, 300, 17)}
    <rect x="26" y="26" width="2348" height="948" fill="none" stroke="{GOLD}" stroke-width="3"/>
    <rect x="38" y="38" width="2324" height="924" fill="none" stroke="{GOLD}" stroke-width="1.4" opacity="0.8"/>

    {nonveg(96, 82, 52)}
    <text x="1200" y="112" font-family="{SANS}" font-weight="700" font-size="36" letter-spacing="5" fill="{GREEN}" text-anchor="middle">M R ENTERPRISE (AGRO PRODUCTS)</text>
    <text x="1200" y="172" font-family="{SERIF}" font-style="italic" font-size="32" fill="{BROWN}" text-anchor="middle">Healthy food comes from healthy farms &#8212; free-range hens, organic feed,</text>
    <text x="1200" y="214" font-family="{SERIF}" font-style="italic" font-size="32" fill="{BROWN}" text-anchor="middle">richer taste and better nutrition in every egg.</text>
    <g transform="translate(2196,70)">{logo(0.42)}</g>
    <path d="M96,262 L2304,262" stroke="{GOLD}" stroke-width="1.6" opacity="0.8"/>

    <!-- col A: nutrition + barcode -->
    {nutrition_table(96, 310, w=600, rh=40, hh=50, fs=25, hfs=22)}
    {barcode(140, 770, 380, 84)}

    <!-- col B: food info -->
    {_block(810, 336, "INGREDIENTS", ["Organic Country Eggs (100%)"])}
    {_block(810, 452, "ALLERGEN DECLARATION", ["Contains Egg"])}
    {_block(810, 568, "STORAGE INSTRUCTIONS", ["Store in a cool and dry place.", "Refrigerate for longer freshness."])}
    {_block(810, 718, "BEST BEFORE", ["Best before 21 days from packing."])}
    {_block(810, 834, "EGG SIZE &amp; COLOUR", ["Large &#8226; Country Brown"])}

    <!-- col C: statutory -->
    {_block(1560, 336, "MANUFACTURER / MARKETER", ["M R Enterprise (Agro Products)", "[Complete Address]"])}
    {_block(1560, 486, "CUSTOMER CARE", ["[Phone] &#8226; [Email]"])}
    <g transform="translate(1560,590)">
      <rect width="128" height="52" rx="8" fill="none" stroke="{GREEN}" stroke-width="3"/>
      <text x="64" y="36" font-family="{SANS}" font-weight="800" font-size="27" fill="{GREEN}" text-anchor="middle">fssai</text>
      <text x="150" y="34" font-family="{SANS}" font-size="25" fill="{GREEN_DK}">Lic. No.: ______________</text>
    </g>
    {_block(1560, 718, "NET QUANTITY", ["6 Eggs / 12 Eggs / 30 Eggs"])}
    <text x="1560" y="852" font-family="{SANS}" font-size="25" fill="{GREEN_DK}">Batch No.: ________  Packed On: ________</text>
    <text x="1560" y="890" font-family="{SANS}" font-size="25" fill="{GREEN_DK}">MRP (Incl. of all Taxes): &#8377; ________</text>

    <!-- QR far right -->
    {qr(2130, 336, 168)}
    <path d="M2070,310 L2070,880" stroke="{GOLD}" stroke-width="1.4" opacity="0.6"/>
    <path d="M770,310 L770,880" stroke="{GOLD}" stroke-width="1.4" opacity="0.6"/>
    <path d="M1520,310 L1520,880" stroke="{GOLD}" stroke-width="1.4" opacity="0.6"/>

    <rect x="0" y="932" width="2400" height="68" fill="{GREEN}"/>
    <rect x="0" y="928" width="2400" height="3" fill="{GOLD_LT}"/>
    <text x="1200" y="976" font-family="{SANS}" font-weight="600" font-size="26" letter-spacing="4" fill="{CREAM}" text-anchor="middle">EGGSHELL ORGANIC &#8226; DAILY PROTEIN, THE NATURAL WAY.</text>
  </g>'''

# ---------------------------------------------------------------- BOTTOM FACE 2400x760
def bottom_face():
    return f'''
  <g>
    <rect width="2400" height="760" fill="url(#kraftg)"/>
    {speckles(2400, 760, 260, 23)}
    <rect x="26" y="26" width="2348" height="708" fill="none" stroke="{GOLD}" stroke-width="3"/>
    <g transform="translate(1130,140)">{logo(0.7)}</g>
    <text x="1200" y="440" font-family="{SERIF}" font-weight="700" font-size="80" fill="{GREEN}" text-anchor="middle">EggShell</text>
    <text x="1196" y="500" font-family="{SANS}" font-weight="600" font-size="34" letter-spacing="10" fill="{GOLD}" text-anchor="middle">ORGANIC</text>
    <text x="1200" y="600" font-family="{SERIF}" font-style="italic" font-size="34" fill="{BROWN}" text-anchor="middle">Daily Protein, The Natural Way.</text>
  </g>'''

# ---------------------------------------------------------------- documents
KRAFT_DEFS = f'''<defs>
    <linearGradient id="kraftg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E2C79C"/><stop offset="0.55" stop-color="{KRAFT}"/><stop offset="1" stop-color="{KRAFT_DK}"/>
    </linearGradient>
  </defs>'''

def ao_overlay(w, h):
    e = max(36, int(min(w, h) * 0.055))  # edge shading depth
    return f'''<defs>
    <linearGradient id="aoV" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2E2008" stop-opacity="0.16"/><stop offset="1" stop-color="#2E2008" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="aoH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#2E2008" stop-opacity="0.16"/><stop offset="1" stop-color="#2E2008" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="aoVb" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#2E2008" stop-opacity="0.16"/><stop offset="1" stop-color="#2E2008" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="aoHr" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#2E2008" stop-opacity="0.16"/><stop offset="1" stop-color="#2E2008" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sheenV" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFF6E0" stop-opacity="0.10"/><stop offset="0.3" stop-color="#FFF6E0" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{e}" fill="url(#aoV)"/>
  <rect y="{h-e}" width="{w}" height="{e}" fill="url(#aoVb)"/>
  <rect width="{e}" height="{h}" fill="url(#aoH)"/>
  <rect x="{w-e}" width="{e}" height="{h}" fill="url(#aoHr)"/>
  <rect width="{w}" height="{h}" fill="url(#sheenV)"/>'''

def panel_doc(w, h, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {KRAFT_DEFS}
{body}
{ao_overlay(w, h)}
</svg>'''

def flat_doc():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="2400" viewBox="0 0 2400 2400">
  <defs>
    <linearGradient id="sheetbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FBF5E7"/><stop offset="1" stop-color="#F0E4CB"/>
    </linearGradient>
  </defs>
  <rect width="2400" height="2400" fill="url(#sheetbg)"/>
  <text x="1200" y="70" font-family="{SANS}" font-weight="600" font-size="30" letter-spacing="6" fill="{BROWN}" text-anchor="middle">EGGSHELL ORGANIC &#8226; PACKAGING ARTWORK &#8226; M R ENTERPRISE (AGRO PRODUCTS)</text>

  <g transform="translate(72,110) scale(0.94)">{front_face()}</g>
  <text x="72" y="1116" font-family="{SANS}" font-weight="700" font-size="26" letter-spacing="4" fill="{BROWN}">FRONT PANEL</text>

  <g transform="translate(72,1160) scale(0.62)">{top_face()}</g>
  <text x="72" y="1678" font-family="{SANS}" font-weight="700" font-size="26" letter-spacing="4" fill="{BROWN}">TOP PANEL</text>

  <g transform="translate(1600,1160) scale(0.4712)">{side_face()}</g>
  <text x="1600" y="1678" font-family="{SANS}" font-weight="700" font-size="26" letter-spacing="4" fill="{BROWN}">SIDE PANEL</text>

  <g transform="translate(2030,1160) scale(0.4712)">{side_face()}</g>
  <text x="2030" y="1678" font-family="{SANS}" font-weight="700" font-size="26" letter-spacing="4" fill="{BROWN}">SIDE PANEL</text>

  <g transform="translate(72,1730)">{declarations_panel()}</g>
  <text x="72" y="2300" font-family="{SANS}" font-weight="700" font-size="26" letter-spacing="4" fill="{BROWN}">BACK PANEL &#8212; STATUTORY DECLARATIONS</text>

  <text x="1200" y="2364" font-family="{SERIF}" font-style="italic" font-size="30" fill="{BROWN}" text-anchor="middle">Daily Protein, The Natural Way.</text>
</svg>'''

def box3d_doc():
    # affine axonometric mapping
    front_m = "matrix(0.604,-0.025,0,0.58,300,700)"
    top_m   = "matrix(0.604,-0.025,-0.1974,0.3553,450,430)"
    side_m  = "matrix(0.1974,-0.3553,0,0.58,1749.6,640)"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="2048" viewBox="0 0 2048 2048">
  <defs>
    <radialGradient id="bg" cx="0.5" cy="0.42" r="0.75">
      <stop offset="0" stop-color="#FBF4E4"/><stop offset="0.72" stop-color="#F1E5CC"/><stop offset="1" stop-color="#E3D2B2"/>
    </radialGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E7D6B7"/><stop offset="1" stop-color="#D5BF98"/>
    </linearGradient>
    <linearGradient id="kraftg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E2C79C"/><stop offset="0.55" stop-color="{KRAFT}"/><stop offset="1" stop-color="{KRAFT_DK}"/>
    </linearGradient>
  </defs>
  <rect width="2048" height="2048" fill="url(#bg)"/>
  <rect y="1380" width="2048" height="668" fill="url(#floor)"/>

  <!-- shadow -->
  <ellipse cx="1080" cy="1330" rx="880" ry="120" fill="#5A431F" opacity="0.28"/>
  <ellipse cx="1080" cy="1318" rx="700" ry="80" fill="#3E2D12" opacity="0.22"/>

  <!-- SIDE -->
  <g transform="{side_m}">{side_face()}
    <rect width="760" height="1000" fill="#000000" opacity="0.30"/></g>
  <!-- TOP -->
  <g transform="{top_m}">{top_face()}
    <rect width="2400" height="760" fill="#FFFFFF" opacity="0.10"/></g>
  <!-- FRONT -->
  <g transform="{front_m}">{front_face()}
    <rect width="2400" height="1000" fill="#000000" opacity="0.05"/></g>

  <!-- box edges -->
  <g stroke="#8A6A38" stroke-width="3" opacity="0.55" fill="none">
    <path d="M300,700 L1749.6,640 M300,700 L450,430 M1749.6,640 L1899.6,370 M450,430 L1899.6,370"/>
    <path d="M300,1280 L1749.6,1220 M1749.6,640 L1749.6,1220 M300,700 L300,1280 M1899.6,370 L1899.6,950 M1749.6,1220 L1899.6,950"/>
  </g>
</svg>'''

with open(os.path.join(OUT, "eggshell-front-flat.svg"), "w") as f:
    f.write(flat_doc())
with open(os.path.join(OUT, "eggshell-box-3d.svg"), "w") as f:
    f.write(box3d_doc())

# per-panel docs for GLB texturing
panels = {
    "panel-front.svg":  panel_doc(2400, 1000, front_face()),
    "panel-back.svg":   panel_doc(2400, 1000, back_face()),
    "panel-top.svg":    panel_doc(2400, 760, top_face()),
    "panel-bottom.svg": panel_doc(2400, 760, bottom_face()),
    "panel-side.svg":   panel_doc(760, 1000, side_face()),
}
for name, doc in panels.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(doc)
print("wrote sheet, box-3d and", len(panels), "panel SVGs")
