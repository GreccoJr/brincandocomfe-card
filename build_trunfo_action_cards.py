#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cartas de AÇÃO do Super Trunfo — design DIFERENTE do álbum.

- Arte de ação full-bleed (assets/trunfo_action/<id>.png) — herói executando o feito.
- Divisória diagonal de "energia" entre a cena e o painel (dá dinamismo).
- Badge HEXAGONAL com o código do grupo (A1–H4) bem visível → modo Quarteto.
- Painel de atributos com cabeçalho "ATRIBUTOS", barras e o destaque em ouro com ★.
- Jesus (H1): moldura/brilho dourado + selo SUPER TRUNFO.

Uso:
  python3 build_trunfo_action_cards.py          # todas as que tiverem arte de ação
  python3 build_trunfo_action_cards.py E3       # só uma
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trunfo_data import cards, ATTRS

BASE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(BASE, "assets", "trunfo_action")
OUT = os.path.join(BASE, "trunfo_action_out")
os.makedirs(OUT, exist_ok=True)
W, H = 760, 1060
GOLD = (238, 202, 128); GOLD_HI = (255, 226, 150); WHITE = (255, 255, 255)
# Avenir via Render Secret File (base64) — repo PÚBLICO, fonte fica privada no Render.
# Decodifica o secret p/ /tmp e usa como fonte primária (= idêntico ao baralho validado).
def _load_avenir_secret():
    out = "/tmp/AvenirNext-Bold.ttf"
    if os.path.exists(out):
        return out
    import base64 as _b64
    paths = ["/etc/secrets/avenir-bold.b64", "avenir-bold.b64",
             "/opt/render/project/src/avenir-bold.b64", os.environ.get("AVENIR_B64", "")]
    for p in paths:
        try:
            if p and os.path.exists(p):
                with open(p) as fh:
                    with open(out, "wb") as o:
                        o.write(_b64.b64decode(fh.read()))
                return out
        except Exception:
            pass
    return None


_load_avenir_secret()


# Ordem de prioridade de fontes (mais próximas de Avenir Next primeiro)
def _find_font():
    candidates = [
        "/tmp/AvenirNext-Bold.ttf",                                    # Avenir via Secret File (decodificado no startup) = idêntico ao baralho
        "/fonts/Mulish-ExtraBold.ttf",                                 # fallback — Mulish ExtraBold (face única, SEMPRE bold; livre OFL)
        "/System/Library/Fonts/Avenir Next.ttc",                       # macOS dev (referência original)
        "/fonts/Mulish-Regular.ttf",                                    # Docker fallback livre — geometric humanist próxima de Avenir
        "/fonts/Manrope-Regular.ttf",                                   # Docker fallback
        "/fonts/Nunito-Regular.ttf",                                    # Docker legacy
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",              # Linux fallback
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise RuntimeError("nenhuma fonte TTF encontrada")

AV = _find_font()


_FACE_IDX = {}


def _ttc_index(style_want):
    """Acha o índice do rosto pelo NOME do estilo (determinístico — independe da
    ordem que cada freetype/Pillow lê a coleção .ttc)."""
    if not _FACE_IDX:
        for i in range(0, 40):
            try:
                _, sty = ImageFont.truetype(AV, 10, index=i).getname()
            except Exception:
                break
            _FACE_IDX.setdefault(sty, i)
    prefs = {
        "Bold": ["Bold", "Demi Bold", "Heavy", "Medium", "Regular"],
        "Regular": ["Regular", "Medium", "Bold"],
    }[style_want]
    for s in prefs:
        if s in _FACE_IDX:
            return _FACE_IDX[s]
    return 0


def font(sz, bold=False):
    # Arquivo de face única já BOLD (Mulish ExtraBold no Render / Avenir Bold extraído) — zero ambiguidade.
    if AV.endswith("-ExtraBold.ttf") or AV.endswith("-Bold.ttf"):
        return ImageFont.truetype(AV, sz)
    # Avenir Next .ttc (dev macOS): o design validado usa o peso BOLD em todo o texto.
    # Seleciona o rosto Bold POR NOME (robusto — independe da ordem da coleção).
    if AV.endswith(".ttc"):
        try:
            return ImageFont.truetype(AV, sz, index=_ttc_index("Bold"))
        except Exception:
            return ImageFont.truetype(AV, sz)
    # Mulish/Manrope/Nunito são variable fonts — peso configurável via font_variation_settings
    f = ImageFont.truetype(AV, sz)
    if bold:
        try:
            f.set_variation_by_axes([700])  # weight=Bold
        except Exception:
            # variant axes não suportados — tenta variante Bold em arquivo separado
            bold_candidates = [
                AV.replace("Regular", "Bold"),
                AV.replace("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"),
                AV.replace("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"),
            ]
            for b in bold_candidates:
                if b != AV and os.path.exists(b):
                    return ImageFont.truetype(b, sz)
    return f


def tsh(d, xy, txt, fnt, fill, anchor="mm", shadow=150):
    d.text((xy[0] + 1, xy[1] + 2), txt, font=fnt, fill=(0, 0, 0, shadow), anchor=anchor)
    d.text(xy, txt, font=fnt, fill=fill, anchor=anchor)


def cover_fit(src, w, h):
    sr, tr = src.width / src.height, w / h
    if sr > tr:
        nh, nw = h, int(h * sr)
    else:
        nw, nh = w, int(w / sr)
    src = src.resize((nw, nh))
    return src.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))


def glass(card, box, radius, tint, alpha):
    x0, y0, x1, y1 = [int(v) for v in box]; w, h = x1 - x0, y1 - y0
    region = card.crop((x0, y0, x1, y1)).convert("RGBA").filter(ImageFilter.GaussianBlur(16))
    region = Image.alpha_composite(region, Image.new("RGBA", (w, h), (tint[0], tint[1], tint[2], alpha)))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    card.paste(region, (x0, y0), mask)


def hexagon(cx, cy, r):
    pts = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def star_points(cx, cy, r, inner=0.46):
    pts = []
    for k in range(5):
        ao = math.radians(-90 + k * 72)
        pts.append((cx + r * math.cos(ao), cy + r * math.sin(ao)))
        ai = math.radians(-90 + k * 72 + 36)
        pts.append((cx + r * inner * math.cos(ai), cy + r * inner * math.sin(ai)))
    return pts


def draw_star(d, cx, cy, r, fill=GOLD_HI, outline=(90, 60, 10, 220), wln=2):
    """Estrela dourada vetorial (não depende de glifo de fonte)."""
    d.polygon(star_points(cx, cy, r), fill=fill, outline=outline)
    if wln:
        d.line(star_points(cx, cy, r) + [star_points(cx, cy, r)[0]], fill=outline, width=wln)


# Subir a arte (px) nas cartas em que a ação estava sendo cortada pelo painel
YSHIFT = {
    "A4": 110,   # Abraão
    "B1": 110,   # Jacó
    "B3": 100,   # Judá
    "E1": 110,   # Samuel
    "E4": 100,   # Salomão
    "F3": 190,   # Daniel
    "H2": 110,   # Pedro
    "H4": 110,   # Paulo
}


def build_card(c, art_path):
    tc, tcd = c["tc"], c["tcd"]
    sup = c["super_trunfo"]
    accent = GOLD if sup else tc

    # fundo: arte de ação full-bleed + scrim no topo
    art = Image.open(art_path).convert("RGB")
    card = cover_fit(art, W, H).convert("RGBA")
    # sobe a arte quando a ação ficou cortada pelo painel (a faixa de baixo fica atrás do painel)
    ys = YSHIFT.get(c["code"], 0)
    if ys:
        shifted = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        shifted.paste(card, (0, -ys))
        # repete a última linha visível p/ não deixar faixa preta na borda do diagonal
        strip = card.crop((0, H - 1, W, H)).resize((W, ys + 4))
        shifted.paste(strip, (0, H - ys - 4))
        card = shifted
    tg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tg)
    for i in range(150):
        td.line([(0, i), (W, i)], fill=(0, 0, 0, int(105 * (1 - i / 150))))
    card = Image.alpha_composite(card, tg)

    # --- painel inferior com divisória DIAGONAL (energia) ---
    PANEL_TOP = 624        # borda direita do diagonal
    DIAG = 64              # quão mais alto começa à esquerda
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    # blur do fundo na região do painel
    region = card.crop((0, PANEL_TOP - DIAG, W, H)).filter(ImageFilter.GaussianBlur(14))
    card.paste(region, (0, PANEL_TOP - DIAG))
    # polígono diagonal preenchido com a cor escura do time
    poly = [(0, PANEL_TOP - DIAG), (W, PANEL_TOP), (W, H), (0, H)]
    pd.polygon(poly, fill=(tcd[0], tcd[1], tcd[2], 205))
    # faixa de acento na borda diagonal
    pd.line([(0, PANEL_TOP - DIAG), (W, PANEL_TOP)], fill=(accent[0], accent[1], accent[2], 255), width=7)
    card = Image.alpha_composite(card, panel)
    d = ImageDraw.Draw(card, "RGBA")

    # --- nome + seleção/ref (logo abaixo da diagonal) ---
    nm = c["name"].upper()
    fs = 64 if len(nm) <= 9 else (50 if len(nm) <= 13 else 38)
    tsh(d, (W // 2, PANEL_TOP + 36), nm, font(fs, True), WHITE)
    sub = f"{c['selecao'].upper()}   ·   {c['ref']}"
    tsh(d, (W // 2, PANEL_TOP + 78), sub, font(22, True), GOLD_HI if sup else GOLD)

    # --- painel de atributos ---
    head_y = PANEL_TOP + 112
    d.text((56, head_y), "ATRIBUTOS", font=font(22, True), fill=(255, 255, 255, 220), anchor="lm")
    d.line([(190, head_y), (W - 56, head_y)], fill=(255, 255, 255, 70), width=2)
    rows_top = head_y + 26
    row_h = (H - 54 - rows_top) // len(ATTRS)
    mx = max(c["attr_list"])
    bar_x0, bar_x1 = 286, W - 96
    for i, a in enumerate(ATTRS):
        val = c["attrs"][a]
        cy = rows_top + i * row_h + row_h // 2
        is_hi = (val == mx)
        if is_hi or sup:
            draw_star(d, 62, cy, 14)
        d.text((84, cy), a, font=font(25, True), fill=WHITE, anchor="lm")
        d.rounded_rectangle([bar_x0, cy - 12, bar_x1, cy + 12], radius=12, fill=(255, 255, 255, 45))
        fillw = int((bar_x1 - bar_x0) * (val / 99))
        bar_col = GOLD if (is_hi or sup) else (tc[0], tc[1], tc[2], 255)
        if fillw > 4:
            d.rounded_rectangle([bar_x0, cy - 12, bar_x0 + max(fillw, 24), cy + 12], radius=12, fill=bar_col)
        tsh(d, (W - 50, cy), str(val), font(38, True), GOLD_HI if (is_hi or sup) else WHITE, anchor="rm")

    # --- badge HEXAGONAL com código (Quarteto) ---
    hx, hy, hr = 86, 88, 58
    hexpts = hexagon(hx, hy, hr)
    d.polygon(hexpts, fill=(tcd[0], tcd[1], tcd[2], 235))
    d.line(hexpts + [hexpts[0]], fill=(accent[0], accent[1], accent[2], 255), width=5)
    tsh(d, (hx, hy - 2), c["code"], font(40, True), WHITE)

    # --- brasão da seleção (topo direito) ---
    if c["crest"] and os.path.exists(c["crest"]):
        cs = 86; cr = Image.open(c["crest"]).convert("RGBA")
        m = min(cr.size)
        cr = cr.crop(((cr.width - m) // 2, (cr.height - m) // 2, (cr.width - m) // 2 + m, (cr.height - m) // 2 + m)).resize((cs, cs))
        cmask = Image.new("L", (cs, cs), 0); ImageDraw.Draw(cmask).ellipse([0, 0, cs - 1, cs - 1], fill=255)
        card.paste(cr, (W - cs - 30, 30), cmask); d = ImageDraw.Draw(card, "RGBA")
        d.ellipse([W - cs - 30, 30, W - 30, 30 + cs], outline=(255, 255, 255, 200), width=3)

    # --- selo SUPER TRUNFO (Jesus) — no TOPO, entre o hexágono e o brasão (não cobre o rosto) ---
    if sup:
        sx0, sx1, sy0, sy1 = W // 2 - 150, W // 2 + 150, 32, 92
        glass(card, (sx0, sy0, sx1, sy1), 30, GOLD, 80)
        d = ImageDraw.Draw(card, "RGBA")
        d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=30, outline=(255, 226, 150, 235), width=3)
        cy = (sy0 + sy1) // 2
        tsh(d, (W // 2, cy), "SUPER TRUNFO", font(28, True), GOLD_HI)
        draw_star(d, sx0 + 26, cy, 13)
        draw_star(d, sx1 - 26, cy, 13)

    # --- moldura externa ---
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fr)
    if sup:
        for k, wdt in [(60, 14), (140, 9), (255, 5)]:
            fd.rounded_rectangle([7, 7, W - 8, H - 8], radius=40, outline=(255, 220, 140, k), width=wdt)
    else:
        fd.rounded_rectangle([7, 7, W - 8, H - 8], radius=40, outline=(tc[0], tc[1], tc[2], 235), width=8)
        fd.rounded_rectangle([14, 14, W - 15, H - 15], radius=34, outline=(255, 255, 255, 70), width=2)
    card = Image.alpha_composite(card, fr)

    rmask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(rmask).rounded_rectangle([0, 0, W - 1, H - 1], radius=40, fill=255)
    card.putalpha(rmask)
    out = os.path.join(OUT, f"trunfoA_{c['code']}_{_slug(c['name'])}.png")
    card.save(out)
    return out


def _slug(name):
    return (name.lower().replace(" ", "_").replace("ã", "a").replace("á", "a").replace("é", "e")
            .replace("í", "i").replace("ô", "o").replace("â", "a").replace("ó", "o").replace("ê", "e"))


def art_for(c):
    # id da arte = basename do caminho do álbum, sem extensão
    aid = os.path.splitext(os.path.basename(c["art"]))[0]
    return os.path.join(ART, aid + ".png")


if __name__ == "__main__":
    allc = cards()
    sel = [c for c in allc if c["code"] == sys.argv[1]] if len(sys.argv) > 1 else allc
    done, skip = 0, []
    for c in sel:
        ap = art_for(c)
        if not os.path.exists(ap):
            skip.append(c["code"]); continue
        build_card(c, ap); done += 1; print("ok", c["code"], c["name"])
    print(f"\n{done} cartas de ação geradas.", f"sem arte ainda: {skip}" if skip else "")
