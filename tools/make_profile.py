"""Generates assets/profile.svg for the GitHub profile: a dark, centered personal page
in the style of a minimal portfolio site, with Inter Display embedded (subset)."""
import base64, io, os, sys
from fontTools.ttLib import TTFont
from fontTools import subset

FONT_DIR = os.path.expanduser("~/Library/Fonts")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "profile.svg")
W = 1200

# ---------------------------------------------------------------- content
NAME = "Numan Shaikh"
HEAD1 = ["AI + product", "@icon", "designer"]
HEAD2 = "for SaaS & web apps"

# Paragraphs: list of (text, style) runs. style: None, "u" (underlined), "b" (brighter)
BODY = [
    [("Hi there, I'm Numan.", "b")],
    [("I'm a product designer with 3+ years of making SaaS and web apps feel simple. "
      "Right now I'm a UI/UX designer at ", None), ("The Design Trip", "u"), (" in Pune, and before that I was at ", None),
     ("Whitedot Adverts", "u"), (".", None)],
    [("I like the messy part: untangling complex problems into flows that feel obvious. "
      "I work end to end, from research, IA and wireframes to polished UI, design systems "
      "and prototypes developers can actually build from.", None)],
    [("Most of my work lives in ", None), ("fintech", "u"), (", ", None), ("ed-tech", "u"), (", ", None),
     ("e-commerce", "u"), (" and ", None), ("HMI", "u"),
     (", where clarity matters more than decoration.", None)],
    [("These days I design with AI in the loop and ship interactive sites and prototypes in ", None),
     ("Framer", "u"), (".", None)],
    [("I studied Design & Applied Arts (BFA) at ", None), ("MIT ADT University", "u"), (".", None)],
    [("Always open to interesting work, freelance projects and good collaborations.", None)],
    [("Let's connect", "b")],
]

# ---------------------------------------------------------------- fonts
fonts = {
    "light": TTFont(f"{FONT_DIR}/InterDisplay-Light.ttf"),
    "regular": TTFont(f"{FONT_DIR}/InterDisplay-Regular.ttf"),
    "semibold": TTFont(f"{FONT_DIR}/InterDisplay-SemiBold.ttf"),
}

def width(text, font, size):
    f = fonts[font]
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    return sum(hmtx[cmap.get(ord(c), cmap[ord("?")])][0] for c in text) * size / upm

def embed(font, chars):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    s = subset.Subsetter(opts)
    f = TTFont(f"{FONT_DIR}/InterDisplay-{font}.ttf")
    s.populate(text=chars)
    s.subset(f)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- layout
parts = []
used = {"light": set(), "regular": set(), "semibold": set()}

def text(x, y, s, font, size, fill, anchor="start", extra=""):
    used[font].update(s)
    parts.append(f'<text x="{x:.1f}" y="{y:.1f}" class="{font[0]}" font-size="{size}" fill="{fill}" '
                 f'text-anchor="{anchor}"{extra}>{esc(s)}</text>')

def pill(cx, y, label):
    w = 30 + 1 + 24 + 1 + width(label, "regular", 12) + 22
    x = cx - w / 2
    parts.append(f'<g class="pill"><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="30" rx="15" '
                 f'fill="#FFFFFF" fill-opacity="0.04" stroke="#FFFFFF" stroke-opacity="0.14"/>')
    parts.append(f'<circle class="dot" cx="{x + 16:.1f}" cy="{y + 15}" r="4" fill="#7A7A80"/>')
    parts.append(f'<line x1="{x + 30:.1f}" y1="{y + 9}" x2="{x + 30:.1f}" y2="{y + 21}" stroke="#FFFFFF" stroke-opacity="0.14"/>')
    tx = x + 39
    parts.append(f'<path d="M{tx:.1f} {y + 11} l6 4 l-6 4z" fill="#BDBDC2"/>')
    parts.append(f'<line x1="{x + 55:.1f}" y1="{y + 9}" x2="{x + 55:.1f}" y2="{y + 21}" stroke="#FFFFFF" stroke-opacity="0.14"/>')
    parts.append("</g>")
    text(x + 64, y + 19.5, label, "regular", 12, "#BDBDC2")

# --- hero
y = 64
pill(W / 2, y, "about")

# avatar: monogram with a slowly turning dashed ring
cy = 238
parts.append(f'''<circle cx="600" cy="{cy}" r="58" fill="url(#avatar)" stroke="#FFFFFF" stroke-opacity="0.10"/>
<circle class="ring" cx="600" cy="{cy}" r="68" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1" stroke-dasharray="2 7" stroke-linecap="round"/>''')
text(600, cy + 13, "NS", "light", 38, "#EDEDED", "middle", ' letter-spacing="1"')
text(600, cy + 104, NAME, "regular", 17, "#CFCFD4", "middle")

# headline with an inline outlined icon
size = 68
ICON = 58
gap = 16
w1 = [width(p, "light", size) - 1.5 * len(p) if p != "@icon" else ICON for p in HEAD1]
total = sum(w1) + gap * 2
x = W / 2 - total / 2
hy = 468
for p, w in zip(HEAD1, w1):
    if p == "@icon":
        ix, iy = x, hy - 52
        parts.append(f'''<g class="spark" transform="translate({ix:.1f} {iy})">
  <rect x="1" y="1" width="{ICON - 2}" height="{ICON - 2}" rx="16" fill="none" stroke="#FFFFFF" stroke-opacity="0.9" stroke-width="2.2"/>
  <path d="M26 12 C27.6 21 29.5 23.4 39 25.5 C29.5 27.6 27.6 30 26 39.5 C24.4 30 22.5 27.6 13 25.5 C22.5 23.4 24.4 21 26 12Z" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linejoin="round"/>
  <path d="M41 37 v9 M36.5 41.5 h9" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
</g>''')
    else:
        text(x, hy, p, "light", size, "#F5F5F7", extra=' letter-spacing="-1.5"')
    x += w + gap
text(600, hy + 80, HEAD2, "light", size, "#F5F5F7", "middle", ' letter-spacing="-1.5"')

# dock
tile, g, pad = 58, 10, 11
icons = ["figma", "framer", "ai", "ps", "ae", "claude", "|", "linkedin", "mail"]
dock_w = pad * 2 + sum(tile if i != "|" else 1 for i in icons) + g * (len(icons) - 1)
dx, dy = W / 2 - dock_w / 2, 646
parts.append(f'''<rect x="{dx:.1f}" y="{dy + 14}" width="{dock_w:.1f}" height="{tile + pad * 2}" rx="26" fill="#000000" opacity="0.6" filter="url(#shadow)"/>
<rect x="{dx:.1f}" y="{dy}" width="{dock_w:.1f}" height="{tile + pad * 2}" rx="26" fill="#18181B" fill-opacity="0.92" stroke="#FFFFFF" stroke-opacity="0.12"/>
<rect x="{dx + 1:.1f}" y="{dy + 1}" width="{dock_w - 2:.1f}" height="{(tile + pad * 2) / 2}" rx="25" fill="url(#dockSheen)"/>''')

def icon(kind, x, y, i):
    t = tile
    o = [f'<g class="bob" style="animation-delay:{i * 0.11:.2f}s"><g transform="translate({x:.1f} {y})">']
    def bg(fill):
        o.append(f'<rect width="{t}" height="{t}" rx="15" fill="{fill}"/>'
                 f'<rect x="0.5" y="0.5" width="{t - 1}" height="{t - 1}" rx="14.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.12"/>')
    if kind == "figma":
        bg("#1E1E1E")
        x0, y0 = 19, 14
        o.append(f'<path d="M{x0 + 5} {y0} h5 v10 h-5 a5 5 0 0 1 0 -10z" fill="#F24E1E"/>'
                 f'<path d="M{x0 + 10} {y0} h5 a5 5 0 0 1 0 10 h-5z" fill="#FF7262"/>'
                 f'<path d="M{x0 + 5} {y0 + 10} h5 v10 h-5 a5 5 0 0 1 0 -10z" fill="#A259FF"/>'
                 f'<circle cx="{x0 + 15}" cy="{y0 + 15}" r="5" fill="#1ABCFE"/>'
                 f'<path d="M{x0 + 5} {y0 + 20} h5 v5 a5 5 0 1 1 -5 -5z" fill="#0ACF83"/>')
    elif kind == "framer":
        bg("#0E0E10")
        o.append('<path transform="translate(15 13) scale(1.35)" d="M4 0h16v8h-8zM4 8h8l8 8H4zM4 16h8v8z" fill="#FFFFFF"/>')
    elif kind in ("ai", "ps", "ae"):
        fill, ink, label = {"ai": ("#330000", "#FF9A00", "Ai"), "ps": ("#001E36", "#31A8FF", "Ps"),
                            "ae": ("#00005B", "#9999FF", "Ae")}[kind]
        bg(fill)
        o.append(f'<rect x="7" y="7" width="{t - 14}" height="{t - 14}" rx="7" fill="none" stroke="{ink}" stroke-width="2"/>')
        used["semibold"].update(label)
        o.append(f'<text x="{t / 2}" y="{t / 2 + 8}" class="s" font-size="22" fill="{ink}" text-anchor="middle" letter-spacing="-0.5">{label}</text>')
    elif kind == "claude":
        bg("#D97757")
        rays = []
        import math
        for k in range(10):
            a = k * math.pi / 5 + 0.2
            r0, r1 = 4, 15 if k % 2 == 0 else 12
            rays.append(f'M{29 + r0 * math.cos(a):.1f} {29 + r0 * math.sin(a):.1f} L{29 + r1 * math.cos(a):.1f} {29 + r1 * math.sin(a):.1f}')
        o.append(f'<path d="{" ".join(rays)}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')
    elif kind == "linkedin":
        bg("#0A66C2")
        used["semibold"].update("in")
        o.append(f'<text x="{t / 2}" y="{t / 2 + 10}" class="s" font-size="30" fill="#FFFFFF" text-anchor="middle" letter-spacing="-1">in</text>')
    elif kind == "mail":
        o.append(f'<rect width="{t}" height="{t}" rx="15" fill="url(#mail)"/>'
                 f'<rect x="0.5" y="0.5" width="{t - 1}" height="{t - 1}" rx="14.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.18"/>')
        o.append('<rect x="13" y="18" width="32" height="23" rx="4" fill="#FFFFFF"/>'
                 '<path d="M14.5 20 L29 31 L43.5 20" fill="none" stroke="#2C8CF4" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append("</g></g>")
    parts.append("".join(o))

x = dx + pad
for i, k in enumerate(icons):
    if k == "|":
        parts.append(f'<line x1="{x:.1f}" y1="{dy + 18}" x2="{x:.1f}" y2="{dy + tile + pad * 2 - 18}" stroke="#FFFFFF" stroke-opacity="0.16"/>')
        x += 1 + g
        continue
    icon(k, x, dy + pad, i)
    x += tile + g

# --- about column
y = dy + tile + pad * 2 + 118
pill(W / 2, y, "hello")
col_w, col_x = 560, W / 2 - 280
y += 30 + 64
size, lh = 18.5, 30
for para in BODY:
    # word-wrap the runs into lines of (text, style) pieces
    lines, line, lw = [], [], 0.0
    for run_text, style in para:
        font = "regular"
        for word in run_text.replace(" ", " \0").split("\0"):
            if not word:
                continue
            ww = width(word, font, size)
            if lw + ww - (width(" ", font, size) if word.endswith(" ") else 0) > col_w and line:
                lines.append(line)
                line, lw = [], 0.0
            if line and line[-1][1] == style:
                line[-1] = (line[-1][0] + word, style)
            else:
                line.append((word, style))
            lw += ww
    if line:
        lines.append(line)
    for ln in lines:
        x = col_x
        spans = []
        for piece, style in ln:
            used["regular"].update(piece)
            fill = {"u": "#F2F2F4", "b": "#F5F5F7"}.get(style, "#A9A9B0")
            visible = piece.rstrip(" ")
            spans.append(f'<tspan fill="{fill}">{esc(piece)}</tspan>')
            if style == "u":
                uw = width(visible, "regular", size)
                parts.append(f'<line x1="{x:.1f}" y1="{y + 4:.1f}" x2="{x + uw:.1f}" y2="{y + 4:.1f}" '
                             f'stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1" stroke-dasharray="1.5 2.5"/>')
            x += width(piece, "regular", size)
        parts.append(f'<text x="{col_x:.1f}" y="{y:.1f}" class="r" font-size="{size}" xml:space="preserve">{"".join(spans)}</text>')
        y += lh
    y += 16

# contact hints under "Let's connect" (the real links sit under the image)
y += 2
hx = col_x
for label in ["LinkedIn", "Email"]:
    used["regular"].update(label)
    parts.append(f'<text x="{hx:.1f}" y="{y:.1f}" class="r" font-size="15" fill="#7E7E86">{label}</text>')
    hx += width(label, "regular", 15) + 22
H = int(y + 90)

# ---------------------------------------------------------------- write
ff = "\n".join(
    f'@font-face {{ font-family: "ID{k[0]}"; src: url(data:font/woff2;base64,{embed(fname, "".join(sorted(used[k])) + " ")}) format("woff2"); }}'
    for k, fname in [("light", "Light"), ("regular", "Regular"), ("semibold", "SemiBold")])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Numan Shaikh. AI + product designer for SaaS and web apps. UI/UX designer at The Design Trip, Pune. Previously Whitedot Adverts. BFA in Design and Applied Arts, MIT ADT University.">
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <radialGradient id="glow" cx="50%" cy="0%" r="60%">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.13"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="avatar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2E2E33"/><stop offset="1" stop-color="#121214"/>
  </linearGradient>
  <linearGradient id="dockSheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.06"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="mail" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#4FB6FF"/><stop offset="1" stop-color="#1A6FF0"/>
  </linearGradient>
  <filter id="shadow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.5 0"/>
  </filter>
  <style>
{ff}
    .l {{ font-family: "IDl", "Inter Display", Inter, -apple-system, "Helvetica Neue", Arial, sans-serif; font-weight: 300; }}
    .r {{ font-family: "IDr", "Inter Display", Inter, -apple-system, "Helvetica Neue", Arial, sans-serif; font-weight: 400; }}
    .s {{ font-family: "IDs", "Inter Display", Inter, -apple-system, "Helvetica Neue", Arial, sans-serif; font-weight: 600; }}
    .bob {{ animation: bob 7s cubic-bezier(.3,0,.2,1) infinite; }}
    .ring {{ transform-origin: 600px 238px; animation: spin 40s linear infinite; }}
    .glow {{ animation: breathe 9s ease-in-out infinite; }}
    .dot {{ animation: blink 3s ease-in-out infinite; }}
    @keyframes bob {{ 0%, 74%, 100% {{ transform: translateY(0); }} 80% {{ transform: translateY(-7px); }} 86% {{ transform: translateY(0); }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes breathe {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.6; }} }}
    @keyframes blink {{ 0%, 100% {{ fill: #7A7A80; }} 50% {{ fill: #3DDC84; }} }}
    @media (prefers-reduced-motion: reduce) {{ .bob, .ring, .glow, .dot {{ animation: none; }} }}
  </style>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="#0B0B0C"/>
  <ellipse class="glow" cx="600" cy="0" rx="760" ry="520" fill="url(#glow)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.035"/>
  {chr(10).join(parts)}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.08"/>
</g>
</svg>
'''
open(OUT, "w").write(svg)
print(OUT, H, f"{len(svg) / 1024:.0f} KB")
