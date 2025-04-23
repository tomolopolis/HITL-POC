FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim AS backend-builder

WORKDIR /app/backend
RUN pip install uv
COPY backend/pyproject.toml ./
RUN uv pip install -r pyproject.toml

FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist/ /usr/share/nginx/html/

# Copy backend
COPY backend/ /app/backend/
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 80

CMD ["/app/start.sh"]