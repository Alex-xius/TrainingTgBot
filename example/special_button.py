from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from environs import Env

env = Env()
env.read_env()

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = env('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()

# Создаем кнопки
contact_btn = KeyboardButton(
    text='Отправить телефон',
    request_contact=True
)
geo_btn = KeyboardButton(
    text='Отправить геолокацию',
    request_location=True
)
poll_btn = KeyboardButton(
    text='Создать опрос/викторину',
    request_poll=KeyboardButtonPollType()
)

# Добавляем кнопки в билдер
kb_builder.row(contact_btn, geo_btn, poll_btn, width=1)

# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Экспериментируем со специальными кнопками',
        reply_markup=keyboard
    )


# Создаем кнопки
poll_btn_2 = KeyboardButton(
    text='Создать опрос',
    request_poll=KeyboardButtonPollType(type='regular')
)
quiz_btn = KeyboardButton(
    text='Создать викторину',
    request_poll=KeyboardButtonPollType(type='quiz')
)
# Инициализируем билдер
poll_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
poll_kb_builder.row(poll_btn_2, quiz_btn, width=1)

# Создаем объект клавиатуры
poll_keyboard: ReplyKeyboardMarkup = poll_kb_builder.as_markup(
    resize_keyboard=True
)

# Этот хэндлер будет срабатывать на команду "/poll"
@dp.message(Command(commands='poll'))
async def process_poll_command(message: Message):
    await message.answer(
        text='Экспериментируем с кнопками опрос/викторина',
        reply_markup=poll_keyboard
    )


if __name__ == '__main__':
    dp.run_polling(bot)
