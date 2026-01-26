from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage
from data.data import token

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=token)

