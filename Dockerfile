FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--preload", "-w", "4", "-b", "0.0.0.0:8000", "__init__:create_app()"]
