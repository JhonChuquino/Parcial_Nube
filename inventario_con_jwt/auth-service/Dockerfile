FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo
COPY . .

# Variable para Flask si la usa
ENV FLASK_ENV=development

EXPOSE 5001

CMD ["python", "run.py"]
