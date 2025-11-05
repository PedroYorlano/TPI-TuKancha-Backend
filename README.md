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
## Clubes
- GET /api/v1/clubes - Listar todos los clubes
- GET /api/v1/clubes/<id> - Obtener un club por ID
- POST /api/v1/clubes - Crear un nuevo club
- PUT /api/v1/clubes/<id> - Actualizar un club
- DELETE /api/v1/clubes/<id> - Eliminar un club