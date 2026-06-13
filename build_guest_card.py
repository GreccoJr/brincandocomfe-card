#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carta-convidado "CRAQUE DA FÉ" — o card personalizado do filho.

Recebe um RETRATO já cartoonizado (foto do filho transformada no estilo Pixar do
deck, via img2img) + nome + título + 5 atributos + cor, e renderiza no MESMO design
das cartas de ação.

Gera DOIS arquivos:
  <out>            = carta LIMPA, alta resolução (só liberar após aprovação/pagamento)
  <out>_preview    = carta com MARCA D'ÁGUA (listras + reinokids.com.br) p/ aprovação no site

Uso (protótipo):
  python3 build_guest_card.py
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# reaproveita os helpers do renderizador das cartas de ação
from build_trunfo_action_cards import (
    font, tsh, cover_fit, glass, draw_star, W, H, GOLD, GOLD_HI, WHITE,
)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "guest_out")
os.makedirs(OUT, exist_ok=True)

ATTRS = ["FÉ", "CORAGEM", "SABEDORIA", "LIDERANÇA", "FORÇA"]


def render_guest_card(portrait_path, name, title, attr_values, tc=(214, 176, 92),
                      tcd=(120, 88, 30), out="craque.png", yshift=0, portrait_scale=0.82):
    """attr_values = lista de 5 inteiros (0-99) na ordem de ATTRS. title = ex. 'O Corajoso'."""
    accent = GOLD
    # fundo: versão BORRADA/escurecida do retrato preenche a carta inteira (sem emendas)
    src = Image.open(portrait_path).convert("RGB")
    bg = cover_fit(src, W, H).filter(ImageFilter.GaussianBlur(30))
    card = bg.convert("RGBA")
    card = Image.alpha_composite(card, Image.new("RGBA", (W, H), (10, 8, 24, 82)))
    # retrato em 1º plano: MENOR, inteiro, com bordas suavizadas (surge do fundo)
    pw = int(W * portrait_scale)
    ph = int(src.height * pw / src.width)
    psrc = src.resize((pw, ph), Image.LANCZOS).convert("RGBA")
    feather = 48
    m = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(m).rectangle([feather, feather, pw - feather, ph - feather], fill=255)
    psrc.putalpha(m.filter(ImageFilter.GaussianBlur(feather * 0.7)))
    card.alpha_composite(psrc, ((W - pw) // 2, 26 + yshift))
    # scrim escuro no topo p/ legibilidade dos selos
    tg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tg)
    for i in range(150):
        td.line([(0, i), (W, i)], fill=(0, 0, 0, int(92 * (1 - i / 150))))
    card = Image.alpha_composite(card, tg)

    # painel diagonal (PADRÃO do deck)
    PANEL_TOP, DIAG = 624, 64
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    region = card.crop((0, PANEL_TOP - DIAG, W, H)).filter(ImageFilter.GaussianBlur(14))
    card.paste(region, (0, PANEL_TOP - DIAG))
    pd.polygon([(0, PANEL_TOP - DIAG), (W, PANEL_TOP), (W, H), (0, H)], fill=(tcd[0], tcd[1], tcd[2], 205))
    pd.line([(0, PANEL_TOP - DIAG), (W, PANEL_TOP)], fill=(accent[0], accent[1], accent[2], 255), width=7)
    card = Image.alpha_composite(card, panel)
    d = ImageDraw.Draw(card, "RGBA")

    # nome + título
    nm = name.upper()
    fs = 64 if len(nm) <= 9 else (50 if len(nm) <= 13 else 38)
    tsh(d, (W // 2, PANEL_TOP + 36), nm, font(fs, True), WHITE)
    tsh(d, (W // 2, PANEL_TOP + 78), title.upper(), font(24, True), GOLD_HI)

    # painel de atributos (padrão do deck)
    head_y = PANEL_TOP + 112
    d.text((56, head_y), "ATRIBUTOS", font=font(22, True), fill=(255, 255, 255, 220), anchor="lm")
    d.line([(190, head_y), (W - 56, head_y)], fill=(255, 255, 255, 70), width=2)
    rows_top = head_y + 26
    row_h = (H - 54 - rows_top) // len(ATTRS)
    mx = max(attr_values)
    bar_x0, bar_x1 = 286, W - 96
    for i, a in enumerate(ATTRS):
        val = attr_values[i]
        cy = rows_top + i * row_h + row_h // 2
        is_hi = (val == mx)
        if is_hi:
            draw_star(d, 62, cy, 14)
        d.text((84, cy), a, font=font(25, True), fill=WHITE, anchor="lm")
        d.rounded_rectangle([bar_x0, cy - 12, bar_x1, cy + 12], radius=12, fill=(255, 255, 255, 45))
        fw = int((bar_x1 - bar_x0) * (val / 99))
        bcol = GOLD if is_hi else (tc[0], tc[1], tc[2], 255)
        if fw > 4:
            d.rounded_rectangle([bar_x0, cy - 12, bar_x0 + max(fw, 24), cy + 12], radius=12, fill=bcol)
        tsh(d, (W - 50, cy), str(val), font(38, True), GOLD_HI if is_hi else WHITE, anchor="rm")

    # badge hexagonal ★ (convidado) — não conflita com A1–H4
    hx, hy, hr = 86, 88, 58
    pts = [(hx + hr * math.cos(math.radians(60 * k - 90)), hy + hr * math.sin(math.radians(60 * k - 90))) for k in range(6)]
    d.polygon(pts, fill=(tcd[0], tcd[1], tcd[2], 235))
    d.line(pts + [pts[0]], fill=(accent[0], accent[1], accent[2], 255), width=5)
    draw_star(d, hx, hy, 26)

    # selo CRAQUE DA FÉ no topo
    sx0, sx1, sy0, sy1 = W // 2 - 165, W // 2 + 165, 32, 92
    glass(card, (sx0, sy0, sx1, sy1), 30, GOLD, 80); d = ImageDraw.Draw(card, "RGBA")
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=30, outline=(255, 226, 150, 235), width=3)
    cy = (sy0 + sy1) // 2
    tsh(d, (W // 2, cy), "CRAQUE DA FÉ", font(28, True), GOLD_HI)
    draw_star(d, sx0 + 26, cy, 13); draw_star(d, sx1 - 26, cy, 13)

    # moldura dourada + cantos arredondados
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fr)
    for k, wln in [(60, 14), (140, 9), (255, 5)]:
        fd.rounded_rectangle([7, 7, W - 8, H - 8], radius=40, outline=(255, 220, 140, k), width=wln)
    card = Image.alpha_composite(card, fr)
    rmask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(rmask).rounded_rectangle([0, 0, W - 1, H - 1], radius=40, fill=255)
    card.putalpha(rmask)

    clean_path = os.path.join(OUT, out)
    card.save(clean_path)
    prev = watermark_preview(card)
    prev_path = os.path.join(OUT, out.replace(".png", "") + "_preview.png")
    prev.save(prev_path)
    return clean_path, prev_path


def watermark_preview(card, text="www.brincandocomfe.com.br"):
    """Versão de APROVAÇÃO: listras brancas diagonais + texto repetido (anti-print)."""
    cw, ch = card.size
    D = int(math.hypot(cw, ch)) + 120
    big = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    bd = ImageDraw.Draw(big)
    f = font(34, True)
    step = 116
    for j, y in enumerate(range(0, D, step)):
        bd.rectangle([0, y, D, y + 16], fill=(255, 255, 255, 42))          # listra branca
        off = -(j % 2) * 220
        bd.text((off, y + 42), (text + "   ") * 8, font=f, fill=(255, 255, 255, 90))  # texto repetido
    rot = big.rotate(30, resample=Image.BICUBIC, expand=False)
    l, t = (rot.width - cw) // 2, (rot.height - ch) // 2
    wm = rot.crop((l, t, l + cw, t + ch))
    out = Image.alpha_composite(card.convert("RGBA"), wm)
    out.putalpha(card.split()[3])  # mantém cantos arredondados
    return out


if __name__ == "__main__":
    # PROTÓTIPO: usa um retrato cartoon do deck como stand-in da "foto cartoonizada do filho"
    stand_in = os.path.join(BASE, "assets", "cards", "35_samuel.png")
    clean, prev = render_guest_card(
        stand_in, name="Lucas", title="O Corajoso",
        attr_values=[72, 95, 60, 80, 88],   # CORAGEM em destaque
        tc=(214, 176, 92), tcd=(120, 88, 30),
        out="craque_lucas.png",
    )
    print("LIMPA  :", clean)
    print("PREVIEW:", prev)
