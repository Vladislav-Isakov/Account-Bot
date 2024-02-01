from typing import Union
from typing_extensions import TypedDict

class CommandData(TypedDict):
    command: Union[str, None]
    template: Union[str, None]
    count_templates: int