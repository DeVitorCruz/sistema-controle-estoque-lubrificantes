import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://lubrificantes_user:omOPGaeMSH8ACFTIJNbB4FpVdiXk6oTd@dpg-crk35d2j1k6c73am9u10-a.oregon-postgres.render.com/lubrificantes')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

