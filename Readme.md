# PlanGym

PlanGym es una aplicación web desarrollada con Flask que permite a los usuarios organizar sus entrenamientos, crear rutinas personalizadas y llevar un seguimiento de su actividad física mediante un calendario.

## Índice

* [Funcionalidades](#funcionalidades)
* [Tecnologías utilizadas](#tecnologías-utilizadas)
* [Estructura del proyecto](#estructura-del-proyecto)
* [Base de datos](#base-de-datos)
* [Ejecución local](#ejecución-local)
* [Despliegue con Docker](#despliegue-con-docker)
* [Uso básico](#uso-básico)
* [Tests](#tests)
* [Problemas encontrados](#problemas-encontrados)
* [Mejoras futuras](#mejoras-futuras)
* [Autor](#autor)

## Funcionalidades

* Registro e inicio de sesión de usuarios.
* Creación, edición, activación y eliminación de rutinas.
* Asignación de ejercicios a distintos días de la semana.
* Consulta de ejercicios mediante la API de wger.
* Ejercicios locales de respaldo en caso de fallo de la API.
* Calendario para marcar entrenamientos realizados.
* Cálculo de rachas de entrenamiento.
* Registro diario de series, repeticiones y peso para los ejercicios del entrenamiento actual.
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

### Requisitos previos

* Git para clonar el repositorio.
* Python 3.12 recomendado para la ejecución local.
* Un navegador web moderno para probar la aplicación.
* Docker Desktop con Docker Compose (opcional, para el despliegue en contenedor).

Las dependencias de Python se encuentran en `app/requirements.txt`: Flask, Flask-SQLAlchemy, Flask-Session, Werkzeug y requests, con sus versiones fijadas en ese archivo.

### Clonar el repositorio

```bash
git clone https://github.com/Yag0lc/PlanGym.git
cd PlanGym
```

Instalar dependencias:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
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

La primera ejecución crea la base de datos SQLite en `data/plangym.db`. La consulta de ejercicios usa la API pública de wger y dispone de ejercicios locales de respaldo.

## Uso básico

1. Abre la aplicación en `http://localhost:8080` y crea una cuenta.
2. Inicia sesión y crea una rutina.
3. Añade ejercicios y asígnalos a los días de entrenamiento.
4. Usa el calendario para marcar las sesiones completadas.
5. Cuando el registro de actividad esté habilitado en la versión que estés probando, guarda las series, repeticiones y peso del entrenamiento.

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

Las pruebas automatizadas se ejecutan con `unittest`, incluido en Python. Para la comprobación manual basta con un navegador web; se puede crear una cuenta, iniciar sesión y recorrer las funciones disponibles.

## Problemas encontrados

Durante el desarrollo surgieron algunos problemas:

* Traducciones incompletas en la API de wger.
* Ejercicios sin imágenes disponibles.
* Reestructuración del sistema de rutinas para organizarlas por días.
* Gestión de sesiones y persistencia de datos.
* Configuración y despliegue mediante Docker.

## Mejoras futuras

* Estadísticas más avanzadas.
* Buscador de ejercicios.
* Mayor cobertura de tests.

## Autor

Yago López
