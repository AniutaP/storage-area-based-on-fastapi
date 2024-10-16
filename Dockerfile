FROM python:3.12-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "storage_area:app", "--host", "0.0.0.0", "--port", "80"]