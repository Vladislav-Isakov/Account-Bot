import logging
from logging.handlers import RotatingFileHandler
import os
from config import Config
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

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

log = logging.getLogger()

file_handler = RotatingFileHandler('logs/bot.log', maxBytes=60240,
                                    backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] [%(module)s]:\n   [MESSAGE]: %(message)s \n      [DIRECTORY]: [%(pathname)s:%(lineno)d] \n         [FUNC]: [%(funcName)s]\n'))
file_handler.setLevel(logging.INFO)

log.addHandler(file_handler)
log.info('Bot startup')

from bot import VKBotCmd, models, errors, alembic_setup, requests_classes