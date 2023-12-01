''''Пример записи собственного фильтра'''
from aiogram.filters import BaseFilter
from aiogram.types import Message

admin_ids: list[int] = [173901673, 178876776, 197177271]

class IsAdmon(BaseFilter):
    def __init__(self, admin_ids) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids