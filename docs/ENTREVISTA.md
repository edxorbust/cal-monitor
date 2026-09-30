# Demostración de Calories Tracker

## Recorrido de 5 minutos

1. Inicia sesión y abre Perfil. Guarda una meta de 2200 kcal y 2500 ml. Explica que son valores de ejemplo elegidos por ti.
2. En Ingredientes, crea «Arroz cocido»: 130 kcal por 100 g; y «Pollo»: 165 kcal por 100 g. Son datos ilustrativos para la demostración.
3. En Comidas, selecciona cálculo con ingredientes. Registra 150 g de arroz y 100 g de pollo: 195 + 165 = 360 kcal.
4. En Actividad, registra una caminata de 30 minutos y 100 kcal estimadas.
5. En Resumen, añade 500 ml de agua. Debe mostrar 360 consumidas, 100 quemadas, 260 netas, 1940 restantes y 500/2500 ml.
6. Recarga: todo persiste en PostgreSQL. Cambia la fecha para mostrar el filtro diario.
7. Edita una cantidad de la comida y observa el nuevo total. Explica que cambiar el catálogo no reescribe las comidas pasadas.

## Cómo se relaciona con el résumé

- Full-stack Django/React: formulario React → Axios → serializer/vista DRF → ORM → PostgreSQL.
- APIs REST: muestra las rutas de auth, ingredients, meals y summary en el README.
- Modelo relacional: usuario/perfil uno a uno; perfil/ingredientes y perfil/comidas uno a muchos; comida/ingredientes mediante MealIngredient, que almacena cantidad y datos históricos.
- Autenticación: JWT en Axios, renovación de access token, rutas protegidas y filtrado por usuario en la API. Ocultar una pantalla no basta para proteger los datos.
- Código modular: api_serializers valida entradas; api_views gestiona HTTP y permisos por propietario; services calcula agregados; hooks compartidos gestionan carga y errores en React.
- Escalabilidad: paginación, prefetch de ingredientes de comidas y agregaciones SQL. Son decisiones de diseño, no una afirmación de haber soportado tráfico masivo.

## Preguntas que conviene practicar

**¿Por qué calcular las calorías en el backend?**
El navegador muestra una estimación, pero el servidor valida cantidades, comprueba que los ingredientes pertenecen al usuario y calcula el total autoritativo. Modificar la petición no permite fijar un total falso para una comida por ingredientes.

**¿Cómo evitas que un usuario lea los datos de otro?**
Las consultas de lista y detalle filtran por el usuario autenticado. Una petición con el ID ajeno recibe 404. Al crear, el perfil se asigna desde la sesión, no desde un ID que envía el navegador.

**¿Qué pasa si cambias las calorías de un ingrediente?**
La comida conserva una copia de los valores usados al registrarla. Solo una edición explícita de sus porciones vuelve a calcularla.

**¿Qué pruebas hiciste?**
Registro, login, renovación de tokens, validación, metas, cálculo por porciones, fechas, edición/borrado, historial y aislamiento de usuarios. La suite se ejecuta en una base temporal; el recorrido de interfaz se verifica también contra PostgreSQL real.

**¿Qué mejorarías después?**
Historial de peso, recetas, mejor tratamiento de zonas horarias, despliegue de producción, recuperación de contraseña, rate limiting, cookies HttpOnly y pruebas de carga.

## Descripción breve en inglés

“Calories Tracker is a React and Django REST application backed by PostgreSQL. Users can manage ingredients, log meals, water and activity, and see daily calorie totals. The backend validates ownership and calculates ingredient-based meals. I separate request validation, API views and summary calculations, and test both the calculations and user isolation.”

Describe solo lo que puedas explicar y demostrar. Si te preguntan por herramientas o ayuda recibida, explica con claridad cómo las utilizaste y cómo verificaste los resultados. No presentes el proyecto como una plataforma de producción ni como una aplicación probada a gran escala.
