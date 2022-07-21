from enum import Enum


class Roles(Enum):
    user = "аутентифицированный пользоветель"
    moderator = "модератор"
    admin = "администратор"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
