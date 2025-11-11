"""
Script de prueba para el sistema de autenticación JWT.

Ejecutar desde la raíz del proyecto:
    python test_auth.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def print_response(response):
    """Helper para imprimir respuestas de forma legible"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print("-" * 50)

def test_auth_flow():
    """Prueba el flujo completo de autenticación"""
    
    print("\n" + "="*50)
    print("PRUEBA 1: Login con credenciales válidas")
    print("="*50)
    
    # 1. Login
    login_data = {
        "email": "admin@clubejemplo.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ Login falló. Asegúrate de tener un usuario con esas credenciales.")
        print("Puedes crear uno creando un club con POST /api/v1/clubes")
        return
    
    tokens = response.json()
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
    
    print("✅ Login exitoso!")
    print(f"Access Token: {access_token[:50]}...")
    print(f"Refresh Token: {refresh_token[:50]}...")
    
    # 2. Obtener usuario actual
    print("\n" + "="*50)
    print("PRUEBA 2: Obtener usuario actual con access token")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ Usuario autenticado correctamente!")
    
    # 3. Acceder a ruta protegida por rol (admin)
    print("\n" + "="*50)
    print("PRUEBA 3: Intentar actualizar club (requiere rol admin)")
    print("="*50)
    
    update_data = {"nombre": "Club Actualizado"}
    response = requests.put(f"{BASE_URL}/clubes/1", json=update_data, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ Ruta protegida por rol funciona!")
    elif response.status_code == 403:
        print("⚠️ No tienes permisos (rol insuficiente)")
    
    # 4. Refrescar token
    print("\n" + "="*50)
    print("PRUEBA 4: Refrescar access token con refresh token")
    print("="*50)
    
    refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
    response = requests.post(f"{BASE_URL}/auth/refresh", headers=refresh_headers)
    print_response(response)
    
    if response.status_code == 200:
        new_access_token = response.json()['access_token']
        print("✅ Token refrescado exitosamente!")
        print(f"Nuevo Access Token: {new_access_token[:50]}...")
    
    # 5. Logout
    print("\n" + "="*50)
    print("PRUEBA 5: Logout")
    print("="*50)
    
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ Logout exitoso!")
    
    # 6. Intentar acceder sin token
    print("\n" + "="*50)
    print("PRUEBA 6: Intentar acceder a ruta protegida sin token")
    print("="*50)
    
    response = requests.put(f"{BASE_URL}/clubes/1", json=update_data)
    print_response(response)
    
    if response.status_code == 401:
        print("✅ Protección funciona! No se permite acceso sin token")
    
    # 7. Login con credenciales inválidas
    print("\n" + "="*50)
    print("PRUEBA 7: Login con credenciales inválidas")
    print("="*50)
    
    bad_login = {
        "email": "admin@clubejemplo.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=bad_login)
    print_response(response)
    
    if response.status_code == 401:
        print("✅ Validación de credenciales funciona!")

if __name__ == "__main__":
    print("\n🔐 INICIANDO PRUEBAS DE AUTENTICACIÓN JWT")
    print("="*50)
    print("Asegúrate de que el servidor Flask esté corriendo en el puerto 5000")
    print("="*50)
    
    try:
        test_auth_flow()
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS!")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar al servidor.")
        print("Asegúrate de que Flask esté corriendo:")
        print("  python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
