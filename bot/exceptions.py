

from typing import Any, Dict


class VkApiError(Exception):
    """
    Базовый - родительский класс ошибок, \n
    которые могут возникнуть во время выполнения работы c VK API
    (https://dev.vk.com/ru/reference/errors)
    """
    pass

class ApiError(VkApiError):
    """ Класс отвечающий за ошибки в API VK, возвращает информацию по возникшей ошибке.
    >>> loop = asyncio.get_event_loop() # получаем цикл событий
    >>> result = loop.run_until_complete(asyncio.gather(task_one, task_two, return_exceptions=True)) # планируем запуск нескольких задач конкурентно и запускаем цикл
    >>> result: [ApiError(), ApiError()] # пример возвращаемого результата, если возникнет ошибка при запросе к API VK
    >>> loop.close() # закрываем цикл событий

    Включает в себя код ошибки и её описание.
    В случае необходимости, можно воспользоваться методом-корутиной try_method и повторить
    запрос к API, который вернул ошибку.
    """

    def __init__(self, *, base_vk_api, method: str, values: Dict[str, Any], error_vk_api: Dict[str, Any]) -> None:
        super().__init__()

        self._api = base_vk_api
        self._method = method
        self._values = values
        self._dict_error = error_vk_api
        self._error_code = error_vk_api['error_code']

    async def try_method(self):
        """Повторить запрос, который завершился неудачей, вернёт корутину"""
        return await self._api._method(self._method, self._values)
    
    # def __repr__(self) -> str:
    #     return (
    #         f'[VK_API_ERROR]: \n      '
    #         f'[ERROR_CODE]: {self._error_code} \n      '
    #         f'[ERROR_MSG]: {self._dict_error["error_msg"]}'
    #     )
    
    def __str__(self):
        return f'[{self._error_code}]: {self._dict_error["error_msg"]}'