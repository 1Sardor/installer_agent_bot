from aiogram import filters, types
import json

with open("data/db.json", "r") as f:
    ROLES = json.load(f)


class IsPublic(filters.Filter):

    async def __call__(self, message: types.Message):
        return message.chat.type in ['group', 'supergroup']


class RoleFilter(filters.Filter):
    def __init__(self, role: str):
        self.role = role

    async def __call__(self, message: types.Message):
        if message.chat.type != "private":
            return False
        role = ROLES.get(str(message.chat.id))
        return role == self.role.lower()


class IsCeo(RoleFilter):
    def __init__(self):
        super().__init__("ceo")


class IsSeller(RoleFilter):
    def __init__(self):
        super().__init__("seller")


class IsAgent(RoleFilter):
    def __init__(self):
        super().__init__("agent")


class IsNotStaff(filters.Filter):
    async def __call__(self, message: types.Message):
        user_id = str(message.from_user.id)
        return user_id not in ROLES and message.chat.type in ['private']
