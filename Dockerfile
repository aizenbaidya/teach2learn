FROM node:22-slim AS frontend
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . /app
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY . /app
COPY --from=frontend /app/static/dist/ ./static/dist/
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
