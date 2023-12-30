import argparse
import inspect
import os
from alembic.util.exc import CommandError
from alembic.config import Config
from alembic import command
from typing import Optional, NoReturn

class AlembicConfig:

    def __init__(self, alembic_ini_path: str, alembic_directory: str) -> NoReturn:
        self._config: str = Config(alembic_ini_path)
        self._config.set_main_option('script_location', alembic_directory)
        self._config.cmd_opts = argparse.Namespace()

class Alembic(AlembicConfig):
    main_directory: str = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

    def __init__(self, directory: Optional[str] = '..', revision: Optional[str] = 'head', sql: Optional[bool] = False, tag: Optional[None] = None) -> NoReturn:
        self._root_directory: str = os.path.join(self.main_directory, directory)
        self._alembic_directory: str = os.path.join(self._root_directory, 'migrations')
        self._ini_path: str = os.path.join(self._root_directory, 'alembic.ini')
        self._revision = revision
        self.sql = sql
        self.tag = tag
        self._command = command
        super().__init__(self._ini_path, self._alembic_directory)
    
    def revision(self, autogenerate: bool = True, head: str = 'head', sql: bool = False) -> NoReturn:
        self._command.revision(self._config, autogenerate=autogenerate, head=head, sql=sql)
    
    def stamp(self, revision: str = 'head', sql: bool = False, tag: Optional[str] = None) -> NoReturn:
        self._command.stamp(self._config, revision, sql, tag)
    
    def downgrade(self, revision: str = -1, sql: bool = False, tag: Optional[str] = None) -> NoReturn:
        self._command.downgrade(self._config, revision, sql, tag)
    
    def upgrade(self, revision: str = 'head', sql: bool = False, tag: Optional[str] = None) -> NoReturn:
        self._command.upgrade(self._config, revision, sql, tag)
    
    def setup(self) -> NoReturn:
        ...

Alembic().revision()

x_arg = 'user_parameter=' + user_parameter

if not hasattr(config.cmd_opts, 'x'):
    if x_arg is not None:
        setattr(config.cmd_opts, 'x', [])
        if isinstance(x_arg, list) or isinstance(x_arg, tuple):
            for x in x_arg:
                config.cmd_opts.x.append(x)
        else:
            config.cmd_opts.x.append(x_arg)
    else:
        setattr(config.cmd_opts, 'x', None)