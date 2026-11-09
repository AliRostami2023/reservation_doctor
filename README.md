# Reservation Doctor API

Django REST API for patient/doctor registration, appointment scheduling, orders, magazine articles, and site content.

## Project layout

- `config/settings/base.py`: shared settings
- `config/settings/dev.py`: local development defaults (SQLite, local cache, local media)
- `config/settings/prod.py`: production configuration (PostgreSQL, Redis/Celery, optional Arvan S3)
- `*/views/`: API views grouped by domain
- `*/serializers.py`: request/response validation and representation
- `*/services/`: business operations
- `*/selectors/`: database read/query logic
- `*/models.py`: Django models
- `*/management/commands/`: seed and maintenance commands

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Keep DJANGO_ENV=dev in .env for local development
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Development uses SQLite and Django's local-memory cache by default. Email is printed to the console and Celery tasks run eagerly by default.

## Production setup

Set `DJANGO_ENV=prod` and provide the required environment variables:

- `SECRET_KEY`
- `ALLOWED_HOSTS` (comma-separated)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_SSLMODE`
- `REDIS_URL` (optional; when present it configures Django cache and Celery defaults)
- Arvan storage variables (`ARVAN_ACCESS_KEY`, `ARVAN_SECRET_KEY`, `ARVAN_BUCKET_NAME`, `ARVAN_ENDPOINT`) to enable remote media storage
- SMTP and SMS provider credentials as needed

Then run:

```bash
DJANGO_ENV=prod python manage.py check --deploy
DJANGO_ENV=prod python manage.py migrate
DJANGO_ENV=prod python manage.py collectstatic --noinput
```

Never commit `.env` or real credentials. `.env.example` contains placeholders only.

## Seed data

Sample data commands are optional and intended for development/demo environments:

```bash
python manage.py seed_users
python manage.py seed_doctors
python manage.py seed_magazines
```

Sample image assets are included in `seed_data/images/` for the doctor and magazine seed commands.

## URL prefixes

Existing API route prefixes have been preserved: `/auth/`, `/app/`, `/blogs/`, `/my-order/`, and the root header/footer routes.
