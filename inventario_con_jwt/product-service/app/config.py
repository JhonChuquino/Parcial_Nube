import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "inventario-postgres")
    DB_NAME = os.getenv("DB_NAME", "inventario_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mi-clave-jwt-super-secreta")
    
