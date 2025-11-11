import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 
        'sqlite:///' + os.path.join(basedir, '..', 'instance/tukancha.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'tu-secret-key-super-segura-cambiala-en-produccion')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora en segundos
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 días en segundos