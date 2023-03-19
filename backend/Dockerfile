FROM python:3.9.7-slim
WORKDIR /backend
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "products.wsgi:application", "--bind", "0:8000"]