import argparse
import inspect
from bot import log
import os
from alembic.util.exc import CommandError
from alembic.config import Config
from alembic import command, runtime
from typing import Optional, NoReturn

class AlembicConfig:

    def __init__(self, alembic_ini_path: str, alembic_directory: str) -> NoReturn:
        self._config: str = Config(alembic_ini_path)
        self._config.set_main_option('script_location', alembic_directory)
        self._config.cmd_opts = argparse.Namespace()

class Alembic(AlembicConfig):

    def __init__(self, directory: str = '..', revision: str = 'head') -> NoReturn:
        self._root_directory: str = os.path.join(
            os.path.dirname(
                os.path.abspath(inspect.stack()[0][1])), 
                directory)
        self._alembic_directory: str = os.path.join(self._root_directory, 'migrations')
        self._ini_path: str = os.path.join(self._root_directory, 'alembic.ini')
        self._revision = revision
        self._command = command
        super().__init__(self._ini_path, self._alembic_directory)
    
    def revision(self, autogenerate: bool = True, head: str = 'head', sql: bool = False) -> NoReturn:
        """Фиксация изменений в модели БД и генерация файла с представлением БД"""
        self._command.revision(self._config, autogenerate=autogenerate, head=head, sql=sql)
    
    def stamp(self, revision: str = 'head', sql: bool = False, tag: Optional[str] = None) -> NoReturn:
        self._command.stamp(self._config, revision, sql, tag)
    
    def downgrade(self, revision: str = -1, sql: bool = False, tag: Optional[str] = None) -> NoReturn:
        """
        Понижение версии БД на 1 уровень - возвращение к прошлой версии модели \n
        По умолчанию уровень понижается на 1, за уровень понижения отвечает revision
        """
        self._command.downgrade(self._config, revision, sql, tag)
    
    def upgrade(self, revision: str = 'head', sql: bool = False, tag: Optional[str] = None) -> NoReturn:
        """Обновление модели БД до последней версии"""
        self._command.upgrade(self._config, revision, sql, tag)
    
    def setup(self) -> NoReturn:
        """
        Отвечает за проверку версии модели БД, если модель была изменена \n
        Фиксирует изменения и обновляет модели до последней версии
        """
        try:
            self.revision()
        except CommandError:
            log.exception('Новых моделей в БД не обнаружено, обновление не требуется.', exc_info=False)
        else:
            self.upgrade()

alembic_main = Alembic()
alembic_main.setup()