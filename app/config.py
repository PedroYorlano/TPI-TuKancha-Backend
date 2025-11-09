import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 
        'sqlite:///' + os.path.join(basedir, '..', 'instance/tukancha.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False