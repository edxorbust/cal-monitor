# Backend local de Calories Tracker

Requisitos: Python 3.14 (verificado) y una base PostgreSQL disponible.

## Preparación

Ejecutar desde la carpeta `backend`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
```

`requirements.txt` declara las dependencias directas; `requirements-lock.txt` guarda las versiones probadas.

Si no existe `.env`, copiar `.env.example` a `.env` y generar una clave con:

```bash
python -c 'import secrets; print(secrets.token_urlsafe(64))'
```

Guardar esa clave en `DJANGO_SECRET_KEY`. En `DATABASE_URL`, guardar la URL pública del servicio PostgreSQL de Railway (`DATABASE_PUBLIC_URL`). Usar el puerto público del proxy. No subir `.env` a Git ni compartirlo. El archivo ya está ignorado.

La URL interna de Railway solo sirve para servicios dentro de su red. Para este backend local se necesita la conexión pública. Si la base fue eliminada, reactivar el servicio y adjuntar el volumen que solicite antes de continuar.

## Comprobar y arrancar

```bash
source .venv/bin/activate
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

`migrate` crea o actualiza las tablas en la base configurada. Usar una base dedicada a esta aplicación. No importar manualmente las tablas.

En otra terminal, desde `frontend`:

```bash
npm ci
npm run dev
```

Abrir `http://localhost:5173/register`. Tras crear la cuenta, la app lleva al login; al iniciar sesión muestra el dashboard. Si Vite usa otro puerto, añadir ese origen a `CORS_ALLOWED_ORIGINS` en `backend/.env` y reiniciar Django. La API puede configurarse con `VITE_API_URL` en `frontend/.env`; por defecto usa `http://localhost:8000/api`.

## Rutas de autenticación

- POST `/api/auth/register/`: username, email, password, password2.
- POST `/api/auth/token/`: username, password.
- POST `/api/auth/token/refresh/`: refresh.
- GET `/api/auth/me/`: token Bearer.

## Pruebas aisladas

```bash
python manage.py test tracker --settings=calorie_tracker.test_settings
python manage.py makemigrations --check --dry-run --settings=calorie_tracker.test_settings
```

Las pruebas usan SQLite en memoria y nunca conectan con Railway. Verifican registro, contraseña, duplicados, login, renovación, permisos y CORS. Falta verificar PostgreSQL real después de configurar la URL.

## Funciones actuales

Perfil/metas, ingredientes, comidas manuales o por ingredientes, agua, actividades y resumen diario están conectados. El registro crea el perfil y las cuentas anteriores lo obtienen al consultar Perfil. Las rutas privadas filtran por propietario.

Consultar el README de la raíz para la API y `docs/ENTREVISTA.md` para una demostración. La app sigue usando un servidor local; antes de desplegar públicamente falta configurar el entorno de producción y rotar cualquier credencial antigua que siga activa.
