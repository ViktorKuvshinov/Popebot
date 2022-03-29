from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import message, user
from aiogram.utils import executor
from key import TOKEN
from model import gtp_space
import logging


API_TOKEN = TOKEN #YOUR TOKEN

STICKER = 'CAACAgIAAxkBAAEEUHdiQzs97AYp_FByq0xBXY7UXoKBygACfQADmS9LCsfb0MCpuOlOIwQ'

#user
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет,\nЯ гененирую тексты в библейском стиле!\n \
        Ты можешь отправить мне слово/фразу/предложение и я выдам тебе сгенерированный текст. \
        Список команд \
         \n/start - перезапуск\n \
         \n/info - расскажу о себе\n \
         \n/help - список доступных команд\n")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("start - перезапуск\n \
                        \n/info - расскажу о себе\n \
                        \n/help - список доступных команд\n")

@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.reply("В основу моего обучения легли: \
                        \n 1) Предобученная модель GPT-2 от Сбербанка - sberbank-ai/rugpt3medium_based_on_gpt2 \n \
                        \n 2) Канонические библейские тексты \n ") 

@dp.message_handler()
async def scale(message: types.Message):

    #Send sticker
    user_id = message.from_user.id
    await bot.send_sticker(user_id, STICKER)
    await message.reply('Мне нужно несколько минут чтобы сгенерировать послание... никуда не уходи!')

    #Generate text
    mes = gtp_space(message.text)
    await message.reply(mes)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)