# Calories Tracker

Aplicación full-stack para registrar comidas, ingredientes, agua y actividad, con objetivos personales y resumen diario.

## Arquitectura

- React + Vite: interfaz, rutas protegidas, formularios y estados de carga/error.
- Axios: comunicación con la API y renovación coordinada de tokens JWT.
- Django REST Framework: autenticación, validación, permisos y cálculo de calorías.
- PostgreSQL en Railway: persistencia relacional y migraciones de Django.

La app se ejecuta localmente. La base está alojada en Railway. El servidor de desarrollo no constituye un despliegue de producción.

## Inicio local

Desde la raíz del repositorio, abrir dos terminales:

```bash
cd backend
source .venv/bin/activate
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

```bash
cd frontend
npm ci
npm run dev
```

Abrir http://localhost:5173. En una instalación nueva, crear el entorno virtual e instalar `backend/requirements-lock.txt`. Consultar `backend/README.md` para configurar `backend/.env` con la URL pública de PostgreSQL y una clave Django. No compartir ni subir `.env`.

## Recorrido

1. Registrarse e iniciar sesión.
2. Guardar nombre, peso/altura opcionales y metas en Perfil.
3. Crear ingredientes indicando calorías por una porción de referencia.
4. Registrar una comida manual o seleccionar ingredientes y cantidades.
5. Añadir agua en Resumen y actividad en Actividad.
6. Cambiar de fecha para consultar registros anteriores y recargar para verificar persistencia.

Las cuentas nuevas tienen metas iniciales editables, no recomendaciones personalizadas.

## Diseño de la API

| Recurso | Métodos | Ruta |
|---|---|---|
| Registro | POST | `/api/auth/register/` |
| Login / renovación | POST | `/api/auth/token/`, `/api/auth/token/refresh/` |
| Cuenta actual | GET | `/api/auth/me/` |
| Perfil y metas | GET, PATCH | `/api/profile/` |
| Ingredientes | GET, POST | `/api/ingredients/` |
| Ingrediente | GET, PATCH, DELETE | `/api/ingredients/{id}/` |
| Comidas | GET, POST | `/api/meals/` |
| Comida | GET, PATCH, DELETE | `/api/meals/{id}/` |
| Agua | GET, POST | `/api/water/` |
| Registro de agua | GET, PATCH, DELETE | `/api/water/{id}/` |
| Actividades | GET, POST | `/api/activities/` |
| Actividad | GET, PATCH, DELETE | `/api/activities/{id}/` |
| Resumen diario | GET | `/api/summary/?date=YYYY-MM-DD` |

Las listas de comidas, agua y actividades aceptan `?date=YYYY-MM-DD`. Usan paginación de 50 registros, hasta 200 por página. El frontend recorre las páginas para no omitir registros en las listas. Todas las rutas de datos exigen JWT y filtran por propietario en el servidor. Las rutas antiguas de recetas y catálogos incompletos no están expuestas en esta versión.

## Modelo y cálculos

`User → UserProfile → Ingredient / CalorieEntry / WaterEntry / BurnedCaloriesEntry`.

Una comida (`CalorieEntry`) contiene filas `MealIngredient`: cada fila relaciona un ingrediente con una cantidad y guarda una copia del nombre, unidad y calorías al registrar. Así, cambiar o borrar un ingrediente del catálogo no modifica comidas históricas. Guardar o editar una comida es una transacción atómica.

- Calorías de una porción = calorías de referencia × cantidad / tamaño de referencia.
- Comida = suma de las calorías de sus porciones, calculadas y redondeadas por el servidor.
- Balance neto = calorías consumidas − quemadas.
- Restantes = meta diaria − consumidas + quemadas.

`services.py` agrega los totales con `SUM` en PostgreSQL. La API rechaza números negativos donde no tienen sentido, porciones cero y valores no finitos. Los registros usan la fecha seleccionada por el cliente; la API usa UTC cuando se omite. Se admite hasta mañana UTC para clientes en husos horarios adelantados.

## Verificación

```bash
cd backend
.venv/bin/python manage.py test tracker --settings=calorie_tracker.test_settings
.venv/bin/python manage.py makemigrations --check --dry-run --settings=calorie_tracker.test_settings
cd ../frontend
npm run lint
npm run build
```

Las pruebas automatizadas usan SQLite temporal; no borran ni crean bases en Railway. También se verificó el flujo visual contra PostgreSQL: login, perfil persistente, ingredientes, comida calculada, actividad y agua.

## Límites actuales

- No hay importación de alimentos, escáner, recetas avanzadas ni historial de peso.
- Las calorías de ingredientes y ejercicio son introducidas por el usuario, no obtenidas de un proveedor externo.
- JWT se almacena en localStorage: una futura versión de producción debería evaluar cookies HttpOnly, protección XSS, límites de intentos y recuperación de cuenta.
- Antes de publicar: configurar HTTPS, servidor de producción, hosts, CORS, DEBUG=False, copias de seguridad y rotar cualquier credencial antigua que haya quedado en el historial Git.
- Hay modelos/vistas del prototipo anterior conservados, pero las rutas activas se definen exclusivamente en `tracker/urls.py`. No se afirma que la aplicación esté probada a gran escala.

## Despliegue en Railway

Consultar `docs/RAILWAY.md`. Los servicios usan Docker, Gunicorn/WhiteNoise para Django y Caddy para React. La preparación local está verificada; el despliegue remoto requiere conectar el repositorio y configurar las variables.
