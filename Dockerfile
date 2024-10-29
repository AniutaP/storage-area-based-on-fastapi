# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем PostgreSQL клиентские инструменты
RUN apt-get update && apt-get install -y postgresql-client

# Копируем код приложения в рабочую директорию
COPY . .

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]