FROM python:3.14-slim

WORKDIR /app

COPY requeriments.txt .
RUN pip install -r requeriments.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]