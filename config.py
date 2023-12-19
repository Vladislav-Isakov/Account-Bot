import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import dotenv_values

config = {
    **dotenv_values(".env")
}

class Config:
    DATABASE_URI = f"postgresql+asyncpg://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False