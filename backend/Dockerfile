FROM python:3.9.7-slim
WORKDIR /backend
COPY . .
RUN pip3 install -r products/requirements.txt --no-cache-dir
CMD ["gunicorn", "products.wsgi:application", "--bind", "0:8000"]