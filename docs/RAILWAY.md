# Desplegar Calories Tracker en Railway

Proyecto: CALORIES_TRACKER
https://railway.com/project/cdb1f181-4137-45f9-9933-7a7ad7a8d838

Repositorio: https://github.com/edxorbust/cal-monitor

## Antes de desplegar

Los cambios están en el equipo local. Railway debe recibirlos: hacer commit y push de los archivos de la aplicación y la configuración de despliegue. No subir `.env`, `.venv`, `node_modules` ni archivos generados. Revisar el diff antes de confirmar el commit. No reutilizar claves antiguas que hayan quedado en el historial Git.

## Servicios

Usar PostgreSQL existente y crear dos servicios vacíos conectados al mismo repositorio. Configurarlos antes de desplegar.

| Configuración | Backend | Frontend |
|---|---|---|
| Root Directory | `/backend` | `/frontend` |
| Config File | `/backend/railway.json` | `/frontend/railway.json` |
| Builder | Dockerfile | Dockerfile |
| Dominio público | Generar en Networking | Generar en Networking |
| Puerto de destino | 8000 | 8080 |

Las rutas de Config File parten de la raíz del repositorio, no de Root Directory. Dejar Build Command y Start Command sin overrides manuales: se usan Dockerfiles y sus comandos. Mantener la comprobación de salud del archivo railway.json.

## Variables del backend

- `DATABASE_URL`: añadir una referencia al `DATABASE_URL` privado del servicio PostgreSQL de este proyecto. Ejemplo si se llama Postgres: `${{Postgres.DATABASE_URL}}`. Elegir la referencia desde Railway para usar el nombre real del servicio.
- `DJANGO_SECRET_KEY`: nueva clave aleatoria de al menos 50 caracteres. Generar localmente con `python3 -c 'import secrets; print(secrets.token_urlsafe(64))'` y guardar solo en Railway.
- `DJANGO_DEBUG=False`.
- `DJANGO_ALLOWED_HOSTS`: dominio público del backend, sin `https://` ni rutas. Railway también se incorpora automáticamente mediante `RAILWAY_PUBLIC_DOMAIN`.
- `CORS_ALLOWED_ORIGINS`: URL HTTPS del frontend, sin barra final.
- `CSRF_TRUSTED_ORIGINS`: URL HTTPS del backend para el admin, y del frontend, separadas por coma.
- `PORT=8000`.
- `WEB_CONCURRENCY=2` (opcional).

Las migraciones se ejecutan automáticamente antes de desplegar. Reutilizan las tablas y datos existentes. No crear otra base ni importar SQL.

## Variables del frontend

- `VITE_API_URL=https://DOMINIO-DEL-BACKEND/api`.
- `PORT=8080`.

No colocar contraseñas ni DATABASE_URL en el frontend. Las variables VITE forman parte del JavaScript público. Cambiar VITE_API_URL requiere reconstruir/redeploy del frontend.

El Dockerfile excluye los `.env` locales, así que la IP de la red doméstica no se incorpora al build. Caddy sirve el resultado de Vite y permite recargar rutas como `/dashboard` sin 404.

## Orden

1. Subir los cambios a GitHub.
2. Configurar ambos servicios y generar sus dominios.
3. Configurar variables con los dominios definitivos y la referencia a PostgreSQL.
4. Desplegar backend. Comprobar `https://DOMINIO-BACKEND/health/` → `{"status":"ok"}`.
5. Desplegar frontend. Comprobar `/health` → `ok`.
6. Probar registro/login, ingredientes, comidas, agua y actividad; recargar `/dashboard`.

## Comprobaciones realizadas localmente

- 15 pruebas backend pasan.
- `manage.py check --deploy` sin advertencias con DEBUG=False.
- Gunicorn arranca en el puerto indicado por PORT.
- Healthcheck devuelve 200; WhiteNoise sirve CSS del admin; API privada responde 401 sin token.
- Frontend: lint y build correctos con URL HTTPS de prueba.

Docker y Caddy no estaban instalados localmente; no se ejecutaron las imágenes completas. Su build y el enrutamiento final deben verificarse en Railway. Todavía no hay un despliegue público confirmado.

## Referencias oficiales

- https://docs.railway.com/guides/django
- https://docs.railway.com/guides/react
- https://docs.railway.com/deployments/monorepo
- https://docs.railway.com/deployments/pre-deploy-command
