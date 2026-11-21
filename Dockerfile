FROM node:22-slim AS assets
WORKDIR /app
COPY package-lock.json package.json vite.config.js ./
RUN npm ci
COPY static ./static
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY --from=assets /app/static/dist ./static/dist
EXPOSE 8000
CMD ["gunicorn", "--preload", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
