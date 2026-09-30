FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-lock.txt ./
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY . .
# Static collection needs settings, but never accesses the production database.
RUN DJANGO_SECRET_KEY=build-only-placeholder-not-used-at-runtime-000000000000000000 DATABASE_URL=postgresql://localhost/build DJANGO_DEBUG=False python manage.py collectstatic --noinput
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
CMD ["sh", "start.sh"]
