FROM node:22-slim AS assets
WORKDIR /app
COPY package-lock.json package.json vite.config.js .
RUN npm ci
COPY static static
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
COPY --from=assets app/static/dist static/dist
RUN rm -rf static/js static/css
RUN rm -f package-lock.json package.json vite.config.js requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]
