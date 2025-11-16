# TPI-TuKancha - Backend

Backend para la aplicación de reserva de canchas deportivas.

## 🚀 Características

- API RESTful para gestión de clubes y canchas
- Base de datos SQL con SQLAlchemy
- Autenticación y autorización (próximamente)
- Documentación de la API (próximamente)

## 🛠️ Requisitos

- Python 3.8+
- pip
- SQLite (para desarrollo)

## 🔧 Instalación

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/PedroYorlano/TPI-TuKancha-Backend]
   cd TPI-TuKancha/TPI-TuKancha-Backend

2. Crear y activar entorno virtual:
    python -m venv venv
    # En mac: source venv/bin/activate  
    # En windows: venv\Scripts\activate

3. Instalar dependencias:
    pip install -r requirements.txt

4. Configurar variables de entorno:
    cp .env.example .env
    # Editar .env según sea necesario

5. Inicializar la base de datos:
    python init_db.py

6. Ejecución
    # Modo desarrollo
    python run.py

    # O usando Flask CLI
    export FLASK_APP=run.py
    export FLASK_ENV=development
    flask run

    # Para debug
    python3 -m flask run --debug

# Estructura del proyecto:
    TPI-TuKancha-Backend/
    ├── app/
    │   ├── api/              # Blueprints y rutas
    │   ├── models/           # Modelos de la base de datos
    │   ├── repositories/     # Capa de acceso a datos
    │   ├── schemas/          # Esquemas para validación
    │   └── services/         # Lógica de negocio
    ├── migrations/           # Migraciones de la base de datos
    ├── tests/                # Pruebas
    ├── .env.example          # Variables de entorno de ejemplo
    ├── config.py             # Configuración de la aplicación
    ├── init_db.py            # Script de inicialización de la BD
    └── requirements.txt      # Dependencias del proyecto

# 📝 API Endpoints

## Autenticación

### `POST /api/v1/auth/login`
Iniciar sesión y obtener tokens de acceso.
- **Body (JSON)**: `{ "email": "string", "password": "string" }`
- **Respuesta (200)**: Tokens de acceso y datos del usuario
- **Roles**: Público

### `POST /api/v1/auth/refresh`
Refrescar token de acceso.
- **Headers**: `Authorization: Bearer <refresh_token>`
- **Respuesta (200)**: Nuevo access token
- **Roles**: Usuarios autenticados

### `GET /api/v1/auth/me`
Obtener información del usuario actual.
- **Headers**: `Authorization: Bearer <access_token>`
- **Respuesta (200)**: Datos del usuario autenticado
- **Roles**: Usuarios autenticados

## Usuarios

### `GET /api/v1/usuarios`
Listar todos los usuarios.
- **Roles**: Admin

### `GET /api/v1/usuarios/<id>`
Obtener usuario por ID.
- **Roles**: Admin, Encargado

### `POST /api/v1/usuarios`
Crear un nuevo usuario.
- **Roles**: Admin

### `PUT /api/v1/usuarios/<id>`
Actualizar un usuario.
- **Roles**: Admin

### `DELETE /api/v1/usuarios/<id>`
Eliminar un usuario.
- **Roles**: Admin

## Clubes

### `GET /api/v1/clubes`
Listar todos los clubes.
- **Roles**: Público

### `GET /api/v1/clubes/<id>`
Obtener un club por ID.
- **Roles**: Público

### `POST /api/v1/clubes`
Crear un nuevo club.
- **Roles**: Admin

### `PUT /api/v1/clubes/<id>`
Actualizar un club.
- **Roles**: Admin, Encargado

### `DELETE /api/v1/clubes/<id>`
Eliminar un club.
- **Roles**: Admin

## Canchas

### `GET /api/v1/canchas`
Listar todas las canchas.
- **Roles**: Público

### `GET /api/v1/canchas/<id>`
Obtener detalles de una cancha.
- **Roles**: Público

### `GET /api/v1/canchas/club/<club_id>`
Obtener canchas por club.
- **Roles**: Usuarios autenticados

### `POST /api/v1/canchas`
Crear una nueva cancha.
- **Roles**: Admin

### `PUT /api/v1/canchas/<id>`
Actualizar una cancha.
- **Roles**: Admin, Encargado

### `DELETE /api/v1/canchas/<id>`
Eliminar una cancha.
- **Roles**: Admin

### `GET /api/v1/canchas/<id>/timeslots`
Obtener timeslots de una cancha.
- **Roles**: Público

## Reservas

### `GET /api/v1/reservas`
Listar todas las reservas.
- **Roles**: Admin, Encargado

### `GET /api/v1/reservas/club/<club_id>`
Obtener reservas por club.
- **Roles**: Admin, Encargado

### `GET /api/v1/reservas/<id>`
Obtener una reserva por ID.
- **Roles**: Admin, Encargado

### `POST /api/v1/reservas`
Crear una nueva reserva.
- **Roles**: Público

### `PUT /api/v1/reservas/<id>/pagar`
Marcar reserva como pagada.
- **Roles**: Admin, Encargado

### `DELETE /api/v1/reservas/<id>`
Cancelar una reserva.
- **Roles**: Admin, Encargado

## Timeslots

### `GET /api/v1/timeslots`
Listar todos los timeslots.
- **Roles**: Público

### `GET /api/v1/timeslots/<id>`
Obtener un timeslot por ID.
- **Roles**: Público

### `POST /api/v1/timeslots`
Crear un nuevo timeslot.
- **Roles**: Admin, Encargado

### `PUT /api/v1/timeslots/<id>`
Actualizar un timeslot.
- **Roles**: Admin, Encargado

### `DELETE /api/v1/timeslots/<id>`
Eliminar un timeslot.
- **Roles**: Admin

## Torneos

### `GET /api/v1/torneos`
Listar todos los torneos.
- **Roles**: Público

### `POST /api/v1/torneos`
Crear un nuevo torneo.
- **Roles**: Admin, Encargado

### `GET /api/v1/torneos/<id>`
Obtener un torneo por ID.
- **Roles**: Público

### `PUT /api/v1/torneos/<id>`
Actualizar un torneo.
- **Roles**: Admin, Encargado

### `DELETE /api/v1/torneos/<id>`
Eliminar un torneo.
- **Roles**: Admin

## Equipos

### `GET /api/v1/equipos`
Listar todos los equipos.
- **Roles**: Público

### `POST /api/v1/equipos`
Crear un nuevo equipo.
- **Roles**: Usuarios autenticados

### `GET /api/v1/equipos/<id>`
Obtener un equipo por ID.
- **Roles**: Público

### `PUT /api/v1/equipos/<id>`
Actualizar un equipo.
- **Roles**: Propietario del equipo

### `DELETE /api/v1/equipos/<id>`
Eliminar un equipo.
- **Roles**: Admin, Propietario del equipo

## Partidos

### `GET /api/v1/partidos`
Listar todos los partidos.
- **Roles**: Público

### `GET /api/v1/partidos/torneo/<torneo_id>`
Obtener partidos por torneo.
- **Roles**: Público

### `GET /api/v1/partidos/equipo/<equipo_id>`
Obtener partidos por equipo.
- **Roles**: Público

### `POST /api/v1/partidos`
Crear un nuevo partido.
- **Roles**: Admin, Encargado

### `PUT /api/v1/partidos/<id>`
Actualizar un partido.
- **Roles**: Admin, Encargado

### `DELETE /api/v1/partidos/<id>`
Eliminar un partido.
- **Roles**: Admin