import asyncio
from copy import deepcopy
from typing import Any, Dict, Optional
from bot.requests_classes import AioLoop, AioRequests
from bot.exceptions import ApiError


class VKApi:

    def __init__(self, *, token: Optional[str] = None, api_version: float = 5.199) -> None:
        self.token = token
        self.api_version = api_version
        self._aio_http = AioRequests
        self._aio_loop = AioLoop()


    async def _method(self, method: str, values: Dict[str, Any]):
        
        values = deepcopy(values) if values else {}

        if 'v' not in values:
            values['v'] = self.api_version

        if any((values.get('access_token'), self.token)):
            values['access_token'] = self.token
        else:
            raise ValueError(f'Отсутствует токен доступа для обращения к API VK.')

        response = await self._aio_http().post(
            'https://api.vk.com/method/' + method,
            data=values
        )

        if response.get('error', None) is not None:

            error = ApiError(base_vk_api=self, method=method, values=values, error_vk_api=response['error'])

            raise error
        
        return response
    
    def method(self, method, values):
        task = self._aio_loop.loop.create_task(self._method(method, values))
        task_2 = self._aio_loop.loop.create_task(self._method(method, values))
        # print(f'Task: {task}')
        # print(f'Task_2: {task_2}')
        try:
            test = self._aio_loop.loop.run_until_complete(asyncio.gather(task, task_2, return_exceptions=True))
            print(test)
        except RuntimeError:
            print('Ошибка')
        self._aio_loop.loop.close()
        return
    
class VkApiMethods:
    """ Позволяет обращаться к методам API через:

    >>> api = VkApiMethod(...)
    >>> api.account.getInfo(fields='...')
    """

    __slots__ = ('_api', '_method')

    def __init__(self, base_vk_api, method=None):
        self._api = base_vk_api
        self._method = method

    def __getattr__(self, method):
        
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])
            
        return VkApiMethods(
            self._api,
            (self._method + '.' if self._method else '') + method
        )

    def __call__(self, **kwargs):

        for key, value in kwargs.items():

            if isinstance(value, (list, tuple)):
                kwargs[key] = ','.join(str(x) for x in value)

        return self._api._method(self._method, kwargs)