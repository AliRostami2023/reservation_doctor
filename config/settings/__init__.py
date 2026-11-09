"""Select settings with DJANGO_ENV=dev|prod (defaults to dev)."""
import os

_environment = os.environ.get("DJANGO_ENV", "dev").strip().lower()
if _environment == "prod":
    from .prod import *  # noqa: F401,F403
elif _environment in {"dev", "development", "local"}:
    from .dev import *  # noqa: F401,F403
else:
    raise RuntimeError("DJANGO_ENV must be one of: dev, prod")
