"""Isolated tests: never connect to or migrate the Railway database."""
import os
os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-secret-with-more-than-fifty-characters-not-for-production")
os.environ["DATABASE_URL"] = "postgresql://localhost/calorie_tracker_tests"
from .settings import *  # noqa: F403, E402
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
