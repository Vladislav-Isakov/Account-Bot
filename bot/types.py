import ast
import re
from typing import (
    Any, 
    Dict, 
    Iterable,
    List, 
    Tuple,
    Union,
    )


class InputTemplateType:

    def __init__(self) -> None:
        """
        :param self.type_variable: все доступные и допустимые типы переменных, для использования в шаблонах команд.
        :param self.type_variable_regex: регулярные выражения, которые будут использоваться при поиске конкретного типа переменной.
        :param self.type_variable_params: доступные параметры для использования в типах данных. \n         Если типа нет, значит он не поддерживает использование параметров и будет выдана ошибка.
        """
        self._PYTHON_CONSTANTS = {"None": None, "True": True, "False": False}
        self.type_variable: Tuple[str] = ('int', 'str', 'float', 'uuid', 'regex')
        self.type_variable_regex: Dict[str, str] = {'int': '\d+', 
                                                    'str': '.*', 
                                                    'float': '\d+.\d+', 
                                                    'uuid': '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
                                                    }
        self.type_variable_regex_length: Dict[str, str] = {'int': '^\d{1,10}$', 
                                                    'str': '^.{1,10}$', 
                                                    'float': '^\d{1,10}.\d{1,10}$', 
                                                    'uuid': '^[a-f0-9]{1,10}-[a-f0-9]{1,10}-[a-f0-9]{1,10}-[a-f0-9]{1,10}-[a-f0-9]{1,10}$'
                                                    }
        self.type_variable_params: Dict[str, Tuple[str, ...]] = {'int': ('length', 'len'), 
                                                                 'str': ('length', 'len'), 
                                                                 'float': ('length', 'len'), 
                                                                 'uuid': ('length', 'len')
                                                                }
        self._part_re = re.compile(
            r"""
            (?:
                (?:\s+)                           
            |
                (?:
                <
                    (?:
                    (?P<command>[a-zA-Z_][a-zA-Z0-9_]*)   # название команды
                    :                                       # разделитель
                    )?
                    (command)
                >
                )
            |
                (?:
                <
                    (?:
                    (?P<type>[a-zA-Z_][a-zA-Z0-9_]*)   # тип переменной
                    (?:\((?P<arguments>.*?)\))?             # аргумент типа переменной
                    :                                       # разделитель переменной
                    )?
                    (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)      # имя переменной
                >
                )
            )
            """,
            re.VERBOSE,
        )

        self._type_args_re = re.compile(
            r"""
            ((?P<name>\w+)\s*=\s*)?
            (?P<value>
                True|False|
                \d+.\d+|
                \d+.|
                \d+|
                [\w\d_.]+|
                [urUR]?(?P<stringval>"[^"]*?"|'[^']*')
            )\s*,
            """,
            re.VERBOSE,
        )

    def _pythonize_command(self, value: str) -> None | bool | int | float | str:
        if value in self._PYTHON_CONSTANTS:
            return self._PYTHON_CONSTANTS[value]
        for convert in int, float:
            try:
                return convert(value)
            except ValueError:
                pass
        if value[:1] == value[-1:] and value[0] in "\"'":
            value = value[1:-1]
        return str(value)

    def _parse_patterns_args(self, argstr: str) -> tuple[Tuple, dict[str, Any]]:
        """
        Ищет аргументы типа в названии команды, например:

        .. code-block:: python

            @bot.command('/<int(length=2):username>')
            def start():
                return "Hello, World!"

        Будет возвращено: (), {'length': 2}

        Пример #2:

            @bot.command('/<int(length=2, custom_param):username>')
            def start():
                return "Hello, World!"

        Будет возвращено: ('custom_param',), {'length': 2}
        """

        argstr += ","
        args = []
        kwargs = {}

        for item in self._type_args_re.finditer(argstr):
            value = item.group("stringval")
            if value is None:
                value = item.group("value")
            value = self._pythonize_command(value)
            if not item.group("name"):
                args.append(value)
            else:
                name = item.group("name")
                kwargs[name] = value

        return tuple(args), kwargs

    def parse_patterns_command(self, bot_command: str) -> Iterable:
        """
        Приставка к переменным t_ - говорит о том, что эта переменная относится к текущему шаблону в итерации.
        """

        command_data: Dict[str, Union[None, str, int]]= {
            "command": None, # название команды - всё что идёт до шаблона <>
            "template": None, # конечный вид команды, после замены на регулярные выражения
            "count_templates": 0 # кол-во шаблонов находящихся в команде
        }

        # Список, в котором будут шаблоны ожидающие замены структуры на регулярное выражение
        replacement_templates: List[Tuple[str, str]] = []

        pos = 0
        while pos < len(bot_command):

            match = self._part_re.match(bot_command, pos)

            if match is None:
                raise ValueError(f"Некорректная структура использованной типизации шаблона в команде: {bot_command!r}") 

            data = match.groupdict()

            name_command = data['command']
            if name_command:
                command_data['command'] = name_command
                replacement_templates.append(
                        (f'<{name_command}:command>', '')
                        )

            pos = match.end()
            if data["type"] is not None:
                if data["type"] not in self.type_variable:
                    raise TypeError(f'В структуре шаблона команды, указан несуществующий тип переменной: {data["type"]!r} \n Существующие типы: {self.type_variable!r}')

                if data["variable"] is not None:
                    
                    t_type_variable = data["type"]
                    t_name_variable = data["variable"]
                    command_data['count_templates'] += command_data['count_templates'] + 1

                    if data["type"] == 'regex':
                        replacement_templates.append(
                                (f'<{t_type_variable}({data["arguments"]}):{t_name_variable}>', data["arguments"])
                                )
                        continue

                    t_args, t_kwargs = self._parse_patterns_args(data["arguments"] or "")

                    if t_args:
                        raise ValueError(f'В структуре шаблона команды указан(ы) недопустимый(е) параметр(ы): {t_args}')

                    replace_template = self.type_variable_regex[t_type_variable]

                    if data["arguments"] is not None and t_kwargs:
                        type_arguments: Union[Tuple[str, ...], None] = self.type_variable_params.get(data["type"], None) # Если в self.type_variable_params у типа переменной нет доступных аргументов, будет None = ошибка 
                        
                        if type_arguments is None:
                            raise ValueError(f'Тип переменной: {data["type"]!r} не может содержать аргументы.')
                        
                        for arg in t_kwargs:
                            if arg not in type_arguments:
                                raise ValueError(f'Тип переменной: {data["type"]!r} не поддерживает аргумент: {arg!r}. \n Поддерживаемые аргументы: {type_arguments!r}')
                            
                            # Связка: название аргумента использованого в типе и его значение, пример:
                            # Шаблон в команде <int(len=10):name>, связка будет: len=10
                            t_params_variable = f'{arg}={t_kwargs[arg]}'

                            # Если в шаблоне используется аргумент указания длины, шаблон регулярного
                            # выражения берётся из отдельно созданного словаря
                            # !!!ВАЖНО!!!
                            # у регулярных выражений без аргумента длины и с аргументом, отличается синтаксис
                            if arg in ['length', 'len']:
                                replace_template = self.type_variable_regex_length[t_type_variable].replace("1,10", f"1,{t_kwargs[arg]}")

                            replacement_templates.append(
                                (f'<{t_type_variable}({t_params_variable}):{t_name_variable}>', replace_template)
                                )
                    else:
                        replacement_templates.append(
                            (
                                f'<{t_type_variable}:{t_name_variable}>',
                                replace_template
                             )
                            )
        data = self._changing_templates(bot_command, replacement_templates)

        if data:
            command_data['template'] = data

        return command_data
    
    def _changing_templates(self, bot_command: str, substitution: List[Tuple[str, str]]):
        """
        Заменяет структуру шаблонов, на регулярные выражения. 
        С помощью регулярок будет поиск  подходящей по шаблону команды с сообщением пользователя.

        Пример:
        .. code-block:: python

            @bot.command('/Начать <regex(^\d{1,10}$):name>', prefixes=['-'])
            def start():
                return "Hello, World!"

            '/Начать <regex(^\d{1,10}$):name>' - структура команды

            substitution = ('<regex(^\d{1,10}$):name>', '^\d{1,10}$')

            Метод вернёт: '/Начать ^\d{1,10}$'
        """

        command = bot_command
        for item in substitution:
            command = command.replace(item[0], item[1])

        return command