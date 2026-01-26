from aiogram import filters, types


class IsGroup(filters.Filter):

    async def __call__(self, message: types.Message):
        return message.chat.type in ['group', 'supergroup']


class IsPrivate(filters.Filter):

    async def __call__(self, message: types.Message):
        return message.chat.type in ['private']

