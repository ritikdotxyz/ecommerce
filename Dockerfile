FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT"]