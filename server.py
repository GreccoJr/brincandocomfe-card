#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Microserviço de geração de cards — Brincando com Fé (Super Trunfo · Card do Filho).

Versão de produção (cloud-ready):
  - PORT vem do env (Render/Railway/Fly definem)
  - CORS habilitado pra brincandocomfe.com.br
  - Opcional: validação por header x-card-token (env CARD_TOKEN)
  - Webhook n8n configurável via env (WEBHOOK_URL)

Endpoints:
  GET  /              -> healthcheck
  GET  /health        -> healthcheck
  POST /api/gerar     -> recebe foto+meta, devolve preview com marca d'água
                         (a versão LIMPA fica em /tmp/, só liberar após pagamento)
"""
import os, sys, io, json, base64, uuid, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_guest_card import render_guest_card

# ===== Config via env =====
PORT          = int(os.environ.get("PORT", "8000"))
WEBHOOK_URL   = os.environ.get(
    "WEBHOOK_URL",
    "https://automatico.projeto.tecnoatende.com.br/webhook/reinokids-card-img2img"
)
CARD_TOKEN    = os.environ.get("CARD_TOKEN", "").strip()  # opcional — se setado, exige no header
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")    # ex: https://brincandocomfe.com.br

# Diretório de saída (efêmero em cloud — limpa ao restart)
OUT_DIR = os.environ.get("OUT_DIR", "/tmp/cards")
os.makedirs(OUT_DIR, exist_ok=True)

CARTOON_PROMPT = (
    "Convert this photo of a child into a stylized 3D animated cartoon character portrait "
    "in the exact same cute Pixar / Disney / DreamWorks kids-movie style: clearly cartoon and stylized, "
    "smooth stylized skin, big friendly expressive eyes, soft rounded child-friendly features, vivid saturated colors, "
    "soft cinematic lighting, warm friendly smile. Keep the child's likeness — same hair color and style, same face. "
    "Upper-body bust, centered, facing camera. NOT photorealistic, not a real photo. "
    "Plain deep gradient background with a soft radial glow behind the character. "
    "No text, no letters, no watermark, no frame, no border."
)

COLORS = {
    "Dourado":  ((214, 176,  92), (120,  88,  30)),
    "Azul":     (( 66, 110, 184), ( 26,  50, 100)),
    "Vermelho": ((192,  72,  60), ( 96,  28,  24)),
    "Verde":    (( 80, 150,  90), ( 28,  72,  40)),
    "Roxo":     ((120,  78, 168), ( 58,  32,  92)),
}


# ===== Helpers =====
def resize_jpeg_b64(raw_bytes, maxdim=1024):
    """Recebe bytes da imagem original, devolve base64 JPEG redimensionado."""
    im = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    if max(im.size) > maxdim:
        r = maxdim / max(im.size)
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


def cartoonize_via_n8n(image_b64):
    """Chama o webhook n8n (Gemini img2img). Devolve base64 PNG do cartoon."""
    body = json.dumps({
        "image_b64": image_b64,
        "mime": "image/jpeg",
        "prompt": CARTOON_PROMPT,
    }).encode()
    req = urllib.request.Request(
        WEBHOOK_URL, data=body, method="POST",
        headers={"Content-Type": "application/json"}
    )
    data = json.loads(urllib.request.urlopen(req, timeout=180).read())
    parts = data["candidates"][0]["content"]["parts"]
    return next(p["inlineData"]["data"] for p in parts if p.get("inlineData"))


# ===== HTTP Handler =====
class Handler(BaseHTTPRequestHandler):
    server_version = "BrincandocomFe-Card/1.0"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Card-Token")

    def _send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self._cors()
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/health", "/healthz"):
            return self._send(200, json.dumps({
                "ok": True,
                "service": "brincandocomfe-card",
                "version": "1.0",
                "webhook_configured": bool(WEBHOOK_URL),
                "token_protection": bool(CARD_TOKEN),
            }))
        return self._send(404, json.dumps({"error": "not_found"}))

    def do_POST(self):
        if self.path != "/api/gerar":
            return self._send(404, json.dumps({"error": "not_found"}))

        # Token check (opcional)
        if CARD_TOKEN:
            sent = self.headers.get("x-card-token", "").strip()
            if sent != CARD_TOKEN:
                return self._send(401, json.dumps({"error": "unauthorized"}))

        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n))

            # Decode foto
            photo_b64 = req["image_b64"].split(",")[-1]  # remove data:image/...;base64,
            raw = base64.b64decode(photo_b64)

            # Resize + cartoonize via Gemini (webhook n8n)
            small = resize_jpeg_b64(raw)
            cartoon_b64 = cartoonize_via_n8n(small)

            # Salva cartoon temporário (insumo do render)
            uid = uuid.uuid4().hex[:10]
            cart_path = os.path.join(OUT_DIR, f"{uid}_cartoon.png")
            with open(cart_path, "wb") as f:
                f.write(base64.b64decode(cartoon_b64))

            # Render da carta "Craque da Fé"
            tc, tcd = COLORS.get(req.get("cor", "Dourado"), COLORS["Dourado"])
            attrs = [max(0, min(99, int(x))) for x in req["attrs"]][:5]

            # CWD precisa ser o dir de saída pra render_guest_card escrever certo
            old_cwd = os.getcwd()
            os.chdir(OUT_DIR)
            try:
                clean, preview = render_guest_card(
                    cart_path,
                    name=req.get("nome", "Herói")[:16],
                    title=req.get("titulo", "O Corajoso")[:22],
                    attr_values=attrs,
                    tc=tc, tcd=tcd,
                    out=f"site_{uid}.png",
                )
            finally:
                os.chdir(old_cwd)

            # Prévia (marca d'água) p/ o navegador + LIMPA (alta) p/ o Vercel guardar no Blob
            with open(preview, "rb") as f:
                prev_b64 = base64.b64encode(f.read()).decode()
            with open(clean, "rb") as f:
                clean_b64 = base64.b64encode(f.read()).decode()

            # Limpa arquivos efêmeros (não precisamos mais)
            for p in (cart_path, preview, clean):
                try: os.remove(p)
                except: pass

            return self._send(200, json.dumps({
                "ok": True,
                "preview_b64": prev_b64,
                "clean_b64": clean_b64,   # versão sem marca d'água — o Vercel guarda no Blob por id
                "id": uid,
            }))

        except urllib.error.HTTPError as e:
            return self._send(502, json.dumps({
                "ok": False,
                "error": "webhook_failed",
                "detalhe": e.read().decode()[:300]
            }))
        except Exception as e:
            return self._send(500, json.dumps({
                "ok": False,
                "error": "internal_error",
                "detalhe": str(e)
            }))

    def log_message(self, fmt, *args):
        # Log simples no stderr (Render/Fly capturam)
        print(f"[{self.address_string()}] {fmt % args}", file=sys.stderr)


def main():
    print(f"=== Brincando com Fé · Card Generator ===", flush=True)
    print(f"PORT={PORT}", flush=True)
    print(f"WEBHOOK_URL={WEBHOOK_URL}", flush=True)
    print(f"CARD_TOKEN={'***' if CARD_TOKEN else '(off)'}", flush=True)
    print(f"ALLOWED_ORIGIN={ALLOWED_ORIGIN}", flush=True)
    print(f"OUT_DIR={OUT_DIR}", flush=True)
    print(f"Servindo em 0.0.0.0:{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
