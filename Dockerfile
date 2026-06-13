FROM python:3.11-slim

# Dependências de sistema (Pillow precisa de libjpeg, zlib etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    fonts-dejavu-core \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Fonte Nunito (Google Fonts, OFL) — usada pelo build_guest_card.py em Linux
RUN mkdir -p /fonts && \
    curl -sSL https://github.com/google/fonts/raw/main/ofl/nunito/Nunito%5Bwght%5D.ttf \
      -o /fonts/Nunito-Regular.ttf && \
    curl -sSL https://github.com/google/fonts/raw/main/ofl/nunito/Nunito-Italic%5Bwght%5D.ttf \
      -o /fonts/Nunito-Italic.ttf

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
