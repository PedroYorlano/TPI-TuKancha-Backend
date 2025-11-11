# 🔐 Guía de Autenticación y Autorización con JWT

## 📚 Índice

1. [¿Cómo funciona?](#cómo-funciona)
2. [Endpoints de autenticación](#endpoints-de-autenticación)
3. [Uso en el Frontend](#uso-en-el-frontend)
4. [Proteger rutas en el Backend](#proteger-rutas-en-el-backend)
5. [Estructura del JWT](#estructura-del-jwt)

---

## 🔍 ¿Cómo funciona?

### Flujo completo:

```
1. Usuario se registra → Se crea un club y usuario admin
2. Usuario hace login → Backend valida credenciales
3. Backend genera 2 tokens:
   - Access Token (1 hora) → Para autenticación en requests
   - Refresh Token (30 días) → Para obtener nuevos access tokens
4. Frontend guarda tokens en localStorage
5. Frontend incluye Access Token en cada request
6. Backend valida token y rol antes de ejecutar la ruta
```

### Componentes:

- **JWT (JSON Web Token)**: Token encriptado que contiene información del usuario
- **Access Token**: Token de corta duración para autenticar requests
- **Refresh Token**: Token de larga duración para renovar access tokens
- **Decoradores**: `@jwt_required()` y `@role_required(['admin'])`

---

## 🌐 Endpoints de Autenticación

### 1. Login (Iniciar Sesión)

**POST** `/api/v1/auth/login`

```json
// Request Body
{
  "email": "admin@clubejemplo.com",
  "password": "password123"
}

// Response 200
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "nombre": "admin",
    "email": "admin@clubejemplo.com",
    "rol": "admin",
    "club_id": 1
  }
}

// Response 401 (Credenciales inválidas)
{
  "error": "Credenciales inválidas"
}
```

### 2. Refresh Token (Renovar Access Token)

**POST** `/api/v1/auth/refresh`

```bash
# Headers
Authorization: Bearer <refresh_token>

# Response 200
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Get Current User (Obtener usuario actual)

**GET** `/api/v1/auth/me`

```bash
# Headers
Authorization: Bearer <access_token>

# Response 200
{
  "id": 1,
  "nombre": "admin",
  "email": "admin@clubejemplo.com",
  "rol": "admin",
  "club_id": 1
}
```

### 4. Logout (Cerrar Sesión)

**POST** `/api/v1/auth/logout`

```bash
# Headers
Authorization: Bearer <access_token>

# Response 200
{
  "message": "Sesión cerrada exitosamente"
}
```

---

## 💻 Uso en el Frontend

### 1. Login

```javascript
// Login
async function login(email, password) {
  const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok) {
    // Guardar tokens en localStorage
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    return data;
  } else {
    throw new Error(data.error);
  }
}
```

### 2. Hacer requests autenticados

```javascript
// Función helper para requests autenticados
async function authenticatedFetch(url, options = {}) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  // Si el token expiró (401), intentar refrescar
  if (response.status === 401) {
    const newToken = await refreshToken();
    if (newToken) {
      // Reintentar el request con el nuevo token
      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${newToken}`,
          "Content-Type": "application/json",
        },
      });
    } else {
      // Si no se puede refrescar, redirigir a login
      window.location.href = "/login";
    }
  }

  return response;
}

// Uso:
const response = await authenticatedFetch(
  "http://127.0.0.1:5000/api/v1/clubes/1",
  {
    method: "PUT",
    body: JSON.stringify({ nombre: "Nuevo Nombre" }),
  }
);
```

### 3. Refrescar token

```javascript
async function refreshToken() {
  const refreshToken = localStorage.getItem("refresh_token");

  const response = await fetch("http://127.0.0.1:5000/api/v1/auth/refresh", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${refreshToken}`,
    },
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
    return data.access_token;
  }

  return null;
}
```

### 4. Logout

```javascript
async function logout() {
  const token = localStorage.getItem("access_token");

  await fetch("http://127.0.0.1:5000/api/v1/auth/logout", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  // Limpiar localStorage
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");

  // Redirigir a login
  window.location.href = "/login";
}
```

---

## 🔒 Proteger Rutas en el Backend

### 1. Ruta protegida con JWT (solo usuarios autenticados)

```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@bp_club.get('/mis-clubes')
@jwt_required()
def mis_clubes():
    current_user_id = get_jwt_identity()
    # Solo usuarios autenticados pueden acceder
    return jsonify({"message": "Ruta protegida"})
```

### 2. Ruta protegida por rol (solo admins)

```python
from flask_jwt_extended import jwt_required
from app.auth.decorators import role_required

@bp_club.delete('/<int:id>')
@jwt_required()
@role_required(['admin'])
def eliminar_club(id):
    # Solo usuarios con rol 'admin' pueden acceder
    club_service.delete(id)
    return '', 204
```

### 3. Ruta protegida por múltiples roles

```python
@bp_club.put('/<int:id>')
@jwt_required()
@role_required(['admin', 'encargado'])
def actualizar_club(id):
    # Admins y encargados pueden acceder
    return jsonify({"message": "Actualizado"})
```

### 4. Obtener información del usuario actual

```python
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

@bp_club.post('/crear-cancha')
@jwt_required()
def crear_cancha():
    # Obtener ID del usuario
    current_user_id = get_jwt_identity()

    # Obtener claims adicionales (rol, club_id, etc.)
    claims = get_jwt()
    user_role = claims.get('rol')
    user_club_id = claims.get('club_id')

    # Usar la información...
    return jsonify({"club_id": user_club_id})
```

### 5. Verificar acceso a datos del propio club

```python
from app.auth.decorators import club_access_required

@bp_club.get('/<int:id>')
@jwt_required()
@club_access_required
def obtener_club(id):
    # Admins: pueden ver cualquier club
    # Otros roles: solo pueden ver su propio club
    club = club_service.get_by_id(id)
    return jsonify(club_schema.dump(club))
```

---

## 🎯 **Estructura del JWT**

Cuando decodificas un access token, contiene:

```json
{
  "sub": "1", // ID del usuario (como STRING)
  "rol": "admin", // Rol del usuario
  "club_id": 1, // ID del club
  "nombre": "Admin", // Nombre del usuario
  "email": "admin@club.com", // Email del usuario
  "exp": 1699564800, // Tiempo de expiración (timestamp)
  "iat": 1699561200, // Tiempo de emisión (timestamp)
  "type": "access" // Tipo de token
}
```

## **⚠️ IMPORTANTE**: El `sub` (subject/identity) es un **string**, no un número. Flask-JWT-Extended requiere que el identity sea string. Si necesitas el ID como número, usa `int(get_jwt_identity())`.

## 🛡️ Niveles de Seguridad

### Público (sin autenticación)

- ✅ Ver lista de clubes
- ✅ Ver detalles de un club
- ✅ Registrar nuevo club
- ✅ Ver canchas de un club

### Autenticado (requiere login)

- ✅ Ver mis reservas
- ✅ Crear reserva
- ✅ Ver mi perfil

### Admin

- ✅ Crear/Editar/Eliminar clubes
- ✅ Ver todos los usuarios
- ✅ Gestionar roles

### Encargado

- ✅ Gestionar canchas de su club
- ✅ Ver reservas de su club
- ✅ Gestionar horarios

### Recepcionista

- ✅ Ver reservas
- ✅ Crear reservas para clientes

---

## 🔧 Configuración

### Variables de entorno (.env)

```bash
# JWT Secret (CAMBIAR EN PRODUCCIÓN)
JWT_SECRET_KEY=tu-secret-key-super-segura-cambiala-en-produccion

# Base de datos
SQLALCHEMY_DATABASE_URI=sqlite:///instance/tukancha.db
```

### Duración de tokens

En `app/config.py`:

```python
JWT_ACCESS_TOKEN_EXPIRES = 3600      # 1 hora
JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 días
```

---

## 🚀 Testing

### Con curl

```bash
# 1. Login
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@clubejemplo.com", "password": "password123"}'

# 2. Usar el token en un request
curl -X GET http://127.0.0.1:5000/api/v1/auth/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."

# 3. Ruta protegida por rol
curl -X DELETE http://127.0.0.1:5000/api/v1/clubes/1 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Con Postman

1. Hacer login en `/api/v1/auth/login`
2. Copiar el `access_token` de la respuesta
3. En requests subsecuentes:
   - Ir a la pestaña "Authorization"
   - Tipo: "Bearer Token"
   - Pegar el access_token

---

## ❓ Preguntas Frecuentes

### ¿Qué pasa si el access token expira?

El frontend debe usar el `refresh_token` para obtener un nuevo `access_token` sin que el usuario tenga que volver a loguearse.

### ¿Cómo implemento logout?

En JWT stateless, el logout se maneja en el cliente eliminando los tokens. El endpoint `/logout` existe para compatibilidad y puede extenderse con una blacklist.

### ¿Puedo cambiar los roles?

Sí, modifica el enum de roles en la base de datos y ajusta los decoradores `@role_required(['rol1', 'rol2'])`.

### ¿Es seguro?

Para desarrollo sí. Para producción:

- Usa HTTPS
- Cambia `JWT_SECRET_KEY` por una clave segura
- Implementa rate limiting
- Considera blacklist de tokens para logout inmediato
