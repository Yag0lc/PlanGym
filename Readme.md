# PlanGym

PlanGym es una aplicación web desarrollada con Flask que permite a los usuarios organizar sus entrenamientos, crear rutinas personalizadas y llevar un seguimiento de su actividad física mediante un calendario.

## Funcionalidades

* Registro e inicio de sesión de usuarios.
* Creación, edición, activación y eliminación de rutinas.
* Asignación de ejercicios a distintos días de la semana.
* Consulta de ejercicios mediante la API de wger.
* Ejercicios locales de respaldo en caso de fallo de la API.
* Calendario para marcar entrenamientos realizados.
* Cálculo de rachas de entrenamiento.
* Perfil de usuario con modificación de datos personales.

## Tecnologías utilizadas

* Python
* Flask
* SQLAlchemy
* SQLite
* HTML
* CSS
* JavaScript
* API de wger
* Docker
* unittest

## Estructura del proyecto

```text
app/
├── client/
├── database/
├── models/
├── repositories/
├── routes/
├── services/
├── static/
├── templates/
└── tests/
```

* **routes**: rutas y controladores Flask.
* **services**: lógica de negocio.
* **repositories**: acceso a datos.
* **models**: modelos de base de datos.
* **templates**: vistas HTML.
* **static**: recursos CSS y JavaScript.
* **client**: integración con APIs externas.

## Base de datos

La aplicación utiliza SQLite para almacenar la información.

Tablas principales:

* Usuarios
* Rutinas
* RutinaEjercicios
* DiasCompletados

## Ejecución local

Instalar dependencias:

```bash
pip install -r app/requirements.txt
```

Ejecutar la aplicación:

```bash
python app/main.py
```

Acceder desde el navegador:

```text
http://localhost:8080
```

## Despliegue con Docker

Construir la imagen:

```bash
docker compose build
```

Iniciar la aplicación:

```bash
docker compose up
```

Acceder desde el navegador:

```text
http://127.0.0.1:8080/
```

Detener los contenedores:

```bash
docker compose down
```

## Tests

Ejecutar los tests:

```bash
python -m unittest discover -s app/tests
```

Actualmente el proyecto incluye 14 tests.

## Problemas encontrados

Durante el desarrollo surgieron algunos problemas:

* Traducciones incompletas en la API de wger.
* Ejercicios sin imágenes disponibles.
* Reestructuración del sistema de rutinas para organizarlas por días.
* Gestión de sesiones y persistencia de datos.
* Configuración y despliegue mediante Docker.

## Mejoras futuras

* Registro de series, repeticiones y pesos.
* Estadísticas más avanzadas.
* Buscador de ejercicios.
* Mayor cobertura de tests.

## Autor

Yago López
