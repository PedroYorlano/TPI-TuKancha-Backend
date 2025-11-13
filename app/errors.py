"""
Define las excepciones personalizadas de la aplicación.
"""

class AppError(Exception):
    """Clase base para todas las excepciones de esta app."""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}

class NotFoundError(AppError):
    """Se lanza cuando un recurso no se encuentra (404)."""
    def __init__(self, message="Recurso no encontrado"):
        super().__init__(message, 404)

class ValidationError(AppError):
    """Se lanza cuando los datos de entrada fallan la validación (400)."""
    def __init__(self, message="Error de validación"):
        super().__init__(message, 400)

class AuthError(AppError):
    """Se lanza para errores de autenticación o permisos (401 o 403)."""
    def __init__(self, message="Error de autenticación"):
        super().__init__(message, 401)

class ConflictError(AppError):
    """Se lanza cuando hay un conflicto con el estado actual (409), ej: email duplicado."""
    def __init__(self, message="Conflicto con recurso existente"):
        super().__init__(message, 409)