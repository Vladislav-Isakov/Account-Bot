import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from config import Config
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

print(sys.argv)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

async_engine = create_async_engine(
    url=Config.DATABASE_URI,
    echo=True,
)

async_session_factory = async_sessionmaker(bind=async_engine)

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/panel.log', maxBytes=60240,
                                    backupCount=10)

from bot import routes, models, errors