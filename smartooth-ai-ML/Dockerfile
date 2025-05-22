# Multi-stage build para reduzir tamanho da imagem final
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Copiar apenas o necessário da etapa de builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Certificar que scripts são executáveis
RUN chmod +x ./scripts/*.sh

# Variáveis de ambiente
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PATH=/root/.local/bin:$PATH

# Portas
EXPOSE 5000  
EXPOSE 8000  

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando de entrada
CMD ["./scripts/start.sh"]