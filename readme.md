# E-Commerce Website (Django)

A simple e-commerce platform built with **Django**, featuring product listings, cart, and order. The project uses Django’s features like models, views, templates, and authentication.

## Features

- User registration & login
- Product catalog with categories
- Add to cart & checkout
- Order history & management

## Docker Installation

1. Clone the repository:

```bash
 git clone https://github.com/ritikdotxyz/ecommerce.git
```

2. Create a .env file

```
#django
SECRET_KEY=""

# stripe
STRIPE_SECRET_KEY=""
STRIPE_PUBLIC_KEY=""

#database
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=""
```

3. Build and start container

```bash
docker-compose up --build
```

## Local Installation

1. Clone the repository:

```bash
 git clone https://github.com/ritikdotxyz/ecommerce.git
```

2. Create a .env file

```
#django
SECRET_KEY=""

# stripe
STRIPE_SECRET_KEY=""
STRIPE_PUBLIC_KEY=""

#database
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=""
```

3. Create virtual environment:

```bash
 python3 -m venv .venv
```

4. Activate virtual environment:

```bash
 python3 -m venv .venv
```

5. Install dependencies:

```bash
 pip install -r requirements.txt
```

6. Start the project:

```bash
 python manage.py runserver
```
