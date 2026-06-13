# Brincando com Fé · Card Generator (microserviço Python)

Microserviço que gera o **Card "Craque da Fé"** (Super Trunfo personalizado com a foto do filho).

Pipeline:
```
navegador
  └─→ POST /api/gerar-card (Vercel Function)
       └─→ POST /api/gerar (este serviço Python)
            ├─ resize foto 1024px
            ├─ chama webhook n8n (Gemini img2img) → cartoon Pixar
            ├─ render_guest_card (PIL) → carta limpa em /tmp/cards/
            └─ retorna preview com marca d'água ao navegador
```

A **versão limpa nunca trafega** antes do pagamento. Só fica em `/tmp/cards/` no servidor.

---

## Estrutura

```
.
├── server.py                       # HTTP server stdlib + ThreadingHTTPServer
├── build_guest_card.py             # Render PIL da carta "Craque da Fé"
├── build_trunfo_action_cards.py    # Helpers (font, glass, draw_star, etc)
├── trunfo_data.py                  # Dados das 33 cartas do baralho base
├── reinokids_data.py               # TEAMS (cores das 8 seleções)
├── requirements.txt                # Pillow
├── Dockerfile                      # Python 3.11-slim + Pillow + Nunito font
├── render.yaml                     # Blueprint Render.com
├── fly.toml                        # Config Fly.io
└── README.md
```

---

## ⚙️ Configuração (env vars)

| Var | Default | Descrição |
|---|---|---|
| `PORT` | `8000` | Porta HTTP |
| `WEBHOOK_URL` | (webhook n8n já configurado) | Endpoint Gemini img2img |
| `CARD_TOKEN` | _(off)_ | Se setado, exige header `x-card-token` em POST `/api/gerar` |
| `ALLOWED_ORIGIN` | `*` | CORS — recomendado `https://brincandocomfe.com.br` |
| `OUT_DIR` | `/tmp/cards` | Saída efêmera das cartas |

---

## 🚀 Deploy — Opção A: Render.com (mais simples, free tier)

1. Cria conta em https://render.com
2. **Faz commit deste diretório num repo GitHub**:
   ```bash
   cd /Users/marcelo/Sites/reinokids-microservice
   git init && git add . && git commit -m "first commit"
   git remote add origin https://github.com/SEU_USER/brincandocomfe-card.git
   git push -u origin main
   ```
3. Render → **New +** → **Blueprint** → conecta o repo → **Apply**
   - Render lê o `render.yaml` e cria o service
4. Painel do service → **Environment** → adiciona:
   - `CARD_TOKEN` = (gera string aleatória forte, ex: `openssl rand -hex 24`)
5. Render builda Docker e sobe. URL final: `https://brincandocomfe-card.onrender.com`

**Limites do free tier:**
- 750h/mês (suficiente pra escala média)
- Dorme após 15min sem uso → primeiro request demora ~30s pra acordar
- Pra evitar dormir: upgrade pra Starter ($7/mês) ou usa Fly.io

---

## 🚀 Deploy — Opção B: Fly.io (mais rápido, $0-3/mês uso leve)

1. Instala flyctl:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```
2. Login:
   ```bash
   flyctl auth login
   ```
3. Cria o app:
   ```bash
   cd /Users/marcelo/Sites/reinokids-microservice
   flyctl launch --no-deploy --copy-config --name brincandocomfe-card
   ```
4. Configura secrets:
   ```bash
   flyctl secrets set CARD_TOKEN="$(openssl rand -hex 24)"
   ```
5. Deploy:
   ```bash
   flyctl deploy
   ```
6. URL: `https://brincandocomfe-card.fly.dev`

**Fly.io vantagens:**
- Região São Paulo (`gru`) — latência baixa pra BR
- Auto-start em ~3s (vs 30s do Render free)
- Free tier: 3 VMs shared-cpu-1x · 256MB RAM
- Custo real estimado: $0-3/mês com tráfego leve

---

## 🔌 Plugar no site (Vercel)

Depois que estiver no ar, configura no projeto Vercel `reinokids`:

```bash
cd /Users/marcelo/Sites/reinokids

# A URL retornada pelo Render/Fly
echo "https://brincandocomfe-card.onrender.com" | \
  vercel env add CARD_GENERATOR_URL production

# Mesmo token que você configurou no microserviço
echo "seu-token-aqui" | \
  vercel env add CARD_GENERATOR_TOKEN production

# Redeploy pra carregar env nova
vercel --prod --yes
```

A partir daí o botão "Gerar Preview" da `/supertrunfo/montar/` funciona end-to-end.

---

## 🧪 Testar localmente

```bash
cd /Users/marcelo/Sites/reinokids-microservice
pip install -r requirements.txt
python3 server.py

# Healthcheck
curl http://localhost:8000/health

# Gerar carta de teste (foto em base64)
PHOTO=$(base64 -i /path/to/foto.jpg)
curl -X POST http://localhost:8000/api/gerar \
  -H "Content-Type: application/json" \
  -d '{
    "image_b64": "data:image/jpeg;base64,'$PHOTO'",
    "nome": "Eloísa",
    "titulo": "A Corajosa",
    "cor": "Dourado",
    "attrs": [96, 82, 88, 80, 60]
  }'
```

---

## 💰 Custo de IA por geração

Cada chamada = **1 imagem Gemini via webhook n8n** já configurado.

- Custo Gemini: ~$0.04 por imagem (Imagen 3) ou ~$0.01-0.02 (Gemini 2.0 Flash)
- Latência típica: 10-30s
- **Margem do produto:** R$ 27 (~$5 USD) por card → ~120-500x markup. Saudável.

---

## ⚖️ LGPD / privacidade

- O servidor recebe a foto, manda pro Gemini via webhook, **deleta** o cartoon temporário após gerar
- **Versão limpa** fica em `/tmp/cards/` (efêmero — limpa ao restart do container)
- Recomendação: implementar cleanup job que apaga PNGs com mais de 24h
- Marca d'água diagonal `www.brincandocomfe.com.br` na prévia (anti-print)

---

## 🐛 Troubleshooting

| Erro | Causa provável | Fix |
|---|---|---|
| `nenhuma fonte TTF encontrada` | Fonte não instalou no Docker | Verificar `RUN curl ... -o /fonts/Nunito-Regular.ttf` no Dockerfile |
| 401 unauthorized | `CARD_TOKEN` não confere | Confirmar header `x-card-token` no Vercel `/api/gerar-card.js` |
| 502 webhook_failed | Webhook n8n offline ou timeout | Conferir `WEBHOOK_URL`; testar direto no n8n |
| Render dorme | Free tier hibernando | Upgrade pra Starter ou usar Fly.io |

---

## Próximos passos sugeridos

- [ ] Após pagamento aprovado no Asaas, gerar download da versão LIMPA via signed URL (S3/R2)
- [ ] Cleanup automático de `/tmp/cards/` > 24h
- [ ] Cache de cartoon por hash da foto (evita regerar se mesma foto sobe 2x)
- [ ] Moderação automática (Google Vision SafeSearch) antes da geração
