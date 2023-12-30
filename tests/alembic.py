import os
import argparse
from alembic.config import Config
from alembic import command
import inspect

def alembic_set_stamp_head(user_parameter):
    # set the paths values
    this_file_directory = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    root_directory      = os.path.join(this_file_directory, '..')
    alembic_directory   = os.path.join(root_directory, 'alembic')
    ini_path            = os.path.join(root_directory, 'alembic.ini')

    # create Alembic config and feed it with paths
    config = Config(ini_path)
    config.set_main_option('script_location', alembic_directory)    
    config.cmd_opts = argparse.Namespace()   # arguments stub

    # If it is required to pass -x parameters to alembic
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

    #prepare and run the command
    revision = 'head'
    sql = False
    tag = None
    command.stamp(config, revision, sql=sql, tag=tag)

    #upgrade command
    command.upgrade(config, revision, sql=sql, tag=tag)