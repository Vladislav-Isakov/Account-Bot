import pytest
from bot.VKBot import Bot

_bot = Bot()

def test_not_command_func():
    with pytest.raises(TypeError):
        _bot.add_command('<test:command>  <int(len=10):name>', prefixes=['-'])


def test_prefix_syntax_error():
    with pytest.raises(TypeError):
        @_bot.command('', prefixes='')
        def command_func():
            ...
        command_func()

def test_unsupported_type_argument():
    with pytest.raises(ValueError):
        @_bot.command('<int(test=10):name>', prefixes=['-', '+'])
        def command_func():
            ...
        command_func()

def test_unsupported_type():
    with pytest.raises(TypeError):
        @_bot.command('<test:name>', prefixes=['-', '+'])
        def command_func():
            ...
        command_func()

def test_invalid_parameters():
    with pytest.raises(ValueError):
        @_bot.command('<int(len=10, 1):name>', prefixes=['-', '+'])
        def command_func():
            ...
        command_func()