FROM python:3.11-slim

# Dependências de sistema (Pillow precisa de libjpeg, zlib etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    fonts-dejavu-core \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Fontes (Google Fonts OFL) — Mulish é a mais próxima de Avenir Next (usada em macOS dev)
# Mantém o layout das cartas idêntico ao baralho original
RUN mkdir -p /fonts && \
    curl -sSL https://github.com/google/fonts/raw/main/ofl/mulish/Mulish%5Bwght%5D.ttf \
      -o /fonts/Mulish-Regular.ttf && \
    curl -sSL https://github.com/google/fonts/raw/main/ofl/mulish/Mulish-Italic%5Bwght%5D.ttf \
      -o /fonts/Mulish-Italic.ttf && \
    # Manrope como fallback secundário (igual ao usado nas LPs Brincando com Fé)
    curl -sSL https://github.com/google/fonts/raw/main/ofl/manrope/Manrope%5Bwght%5D.ttf \
      -o /fonts/Manrope-Regular.ttf

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY *.py ./

# Diretório efêmero pra outputs temporários
RUN mkdir -p /tmp/cards
ENV OUT_DIR=/tmp/cards
ENV PORT=8000
ENV ALLOWED_ORIGIN=https://brincandocomfe.com.br

EXPOSE 8000

# Healthcheck pro orquestrador
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -sf http://localhost:${PORT}/health || exit 1

CMD ["python", "server.py"]
