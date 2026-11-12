from .base import * 

DEBUG = False
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)

# PostgreSQL is configured with individual variables (compatible with Neon).
if config("DB_ENGINE", default="postgresql") in {"postgres", "postgresql"}:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"), "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"), "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="5432"),
        "CONN_MAX_AGE": config("DB_CONN_MAX_AGE", default=60, cast=int),
        "OPTIONS": {"sslmode": config("DB_SSLMODE", default="require")},
    }}

redis_url = config("REDIS_URL", default="")
if redis_url:
    CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": redis_url,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}
    CELERY_BROKER_URL = (config("CELERY_BROKER_URL", default="") or redis_url)
    CELERY_RESULT_BACKEND = (config("CELERY_RESULT_BACKEND", default="") or redis_url)

arvan_access = config("ARVAN_ACCESS_KEY", default="")
arvan_secret = config("ARVAN_SECRET_KEY", default="")
arvan_bucket = config("ARVAN_BUCKET_NAME", default="")
arvan_endpoint = config("ARVAN_ENDPOINT", default="")
if all((arvan_access, arvan_secret, arvan_bucket, arvan_endpoint)):
    AWS_ACCESS_KEY_ID = arvan_access
    AWS_SECRET_ACCESS_KEY = arvan_secret
    AWS_STORAGE_BUCKET_NAME = arvan_bucket
    AWS_S3_ENDPOINT_URL = arvan_endpoint
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    MEDIA_URL = f"https://{arvan_bucket}.{arvan_endpoint.removeprefix('https://').rstrip('/')}/"

CORS_ALLOW_ALL_ORIGINS = False
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
