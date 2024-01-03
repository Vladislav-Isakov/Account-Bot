from functools import update_wrapper
from typing import (
    Any,
    Callable,
    TypeVar,
    cast
)

F = TypeVar("F", bound=Callable[..., Any])

def setupmethod(func: F) -> F:

    def wrapper_func(self, *args: Any, **kwargs: Any) -> Any:
        return func(self, *args, **kwargs)

    return cast(F, update_wrapper(wrapper_func, func))

def _name_from_func(command_func: Callable) -> str:
    """
    Возвращает имя функции.
    """
    assert command_func is not None, "ожидаемая функция, если команда не указана."
    return command_func.__name__

class Scaffold:

    def __init__(self) -> None:
        self.view_functions: dict[str, Callable] = {} # функции - представления, ассоциация с названиями функций, для будущих вызовов
        self.reg_command_functions: dict[str, Callable] = {} # зарегистрированные функции команд

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"
    
    def _method_command(
        self,
        method: str,
        command: str,
        options: dict,
    ) -> Callable:
        if "prefixes" in options:
            raise TypeError("Используйте декоратор 'command' чтобы использовать аргумент 'prefixes'")
        
        return self.command(command, prefixes=[method], **options)
    
    @setupmethod
    def command(self, command: str, **options: Any) -> Callable:
        """
        Задекарируйте функцию команды, чтобы зарегистрировать ее с помощью заданной команды, и укажите параметры.
        Вызывает :meth:`add_command`, который содержит больше подробностей о реализации.

        .. code-block:: python

            @bot.command("/")
            def start():
                return "Hello, World!"



        Имя конечной точки для команды по умолчанию равно имени функции представления, 
        если параметр ``endpoint`` не передан. 

        Параметру ``prefixes`` по умолчанию присвоено значение `["/"]`.

        :param self: :class: VKBot.Bot
        :param command: Команда, закреплённая за конкретной функцией.
        :param options: Дополнительные параметры гибкой настройки.

        """

        def decorator(func: Callable) -> Callable:

            endpoint = options.pop("endpoint", None)

            # Используется метод класса Bot
            # Параметр endpoint будет по умолчанию None
            self.add_command(command, endpoint, func, **options)
            return func
        return decorator
    
    @setupmethod
    def add_command(
        self,
        command: str,
        endpoint: str | None = None,
        command_func: Callable | None = None,
        **options: Any,
    ) -> None:
        """Зарегистрируйте команду для последующей маршрутизации при обработке событий
        Декоратор :meth:`command` — это ярлык для вызова этой команды.
        с аргументом ``command_func``. \n
        Это эквивалентно:

        .. code-block:: python

            @bot.command("/")
            def start():
                ...


            def start():
                ...

            bot.add_command("/", command_func=start)

        Имя конечной точки для команды по умолчанию равно имени функции представления, 
        если параметр ``endpoint`` не передан. 
        Будет выдана ошибка, если функция уже зарегистрирована для конечной точки.

        Параметру ``prefixes`` по умолчанию присвоено значение `["/"]`.


        .. code-block:: python

            bot.add_command("/", endpoint="start")

            @bot.endpoint("start")
            def start():
                ...
        """
        raise NotImplementedError

    def add(self) -> None:
        ...
    
class Bot(Scaffold):

    def __init__(self) -> None:
        super().__init__()
        
    @setupmethod
    def add_command(
        self,
        command: str,
        endpoint: str | None = None,
        command_func: Callable | None = None,
        **options: Any,
    ) -> None:
        print(endpoint)
        if endpoint is None:
            endpoint = _name_from_func(command_func)

        options["endpoint"] = endpoint
        prefixes = options.pop("prefixes", None)

        # если префиксы не заданы, но объект command_func знает их,
        # используются префиксы из объекта command_func. Если ни того, ни другого не существует, 
        #будет кортеж только из ``/`` по умолчанию.
        if prefixes is None:
            prefixes = getattr(command_func, "prefixes", None) or ("/",)
        if isinstance(prefixes, str):
            raise TypeError(
                "Разрешенные префиксы должны представлять собой список строк, например"
                ' example: @bot.command(..., prefixes=["/"])'
            )
        prefixes = {item.upper() for item in prefixes}

        # Префиксы, которые всегда следует добавлять
        required_prefixes = set(getattr(command_func, "required_prefixes", ()))

        # Добавление обязательных префиксов по умолчанию.
        prefixes |= required_prefixes
        # command = self.(command, prefixes=prefixes, **options)

        # self.add(command)
        if command_func is not None:

            old_func = self.view_functions.get(endpoint)

            if old_func is not None and old_func != command_func:
                raise AssertionError(
                    "Сопоставление функций команд перезаписывает существующее"
                    f" командная функция: {endpoint}"
                )
            self.view_functions[endpoint] = command_func