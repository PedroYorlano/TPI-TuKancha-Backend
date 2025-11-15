import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 
        'sqlite:///' + os.path.join(basedir, '..', 'instance/tukancha.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dsasdasd32e453rtfqwetf312478')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora en segundos
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 días en segundos
    
    # Configuración Mercado Pago
    MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN', '')
    MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY', '')
    # URL base del frontend para las redirecciones después del pago
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    # URL base del backend para webhooks
    BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')