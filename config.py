# class Config:
#     SECRET_KEY = 'your_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///lubrificantes.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://lubrificantes_user:omOPGaeMSH8ACFTIJNbB4FpVdiXk6oTd@dpg-crk35d2j1k6c73am9u10-a.oregon-postgres.render.com/lubrificantes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False