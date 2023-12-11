from aiogram import Bot, Dispatcher, F
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaAudio,
                           InputMediaDocument, InputMediaPhoto,
                           InputMediaVideo, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
from environs import Env

env = Env()
env.read_env()

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = env('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


LEXICON: dict[str, str] = {
    'audio': '🎶 Аудио',
    'text': '📃 Текст',
    'photo': '🖼 Фото',
    'video': '🎬 Видео',
    'document': '📑 Документ',
    'voice': '📢 Голосовое сообщение',
    'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
    'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
    'photo_id1': 'AgACAgIAAxkBAAICxWVvfN9QJTTcIQVPQCTtnMbbnwdRAAKa1zEb2GN5S-6STPbilHuhAQADAgADcwADMwQ',
    'photo_id2': 'AgACAgIAAxkBAAICxmVvfPBo0PHTmAkKK-0Hf91Gaqy9AAKZ1zEb2GN5SyFJptclcT_-AQADAgADcwADMwQ',
    'voice_id1': 'AwACAgIAAxkBAAICzWVvfbVlk-ZDbajZSsx1i17qGbPsAAIjQQAC2GN5Sz_YgqZPTjoZMwQ',
    'voice_id2': 'AwACAgIAAxkBAAICzmVvfbie8f33DIPD3dbU3SGUXQiOAAIkQQAC2GN5S5ca-nyr8bhWMwQ',
    'audio_id1': 'CQACAgIAAxkBAAICx2VvfTEcepXri6jBXoovdtdVMpl9AAIbQQAC2GN5S3vzQU3uI40jMwQ',
    'audio_id2': 'CQACAgIAAxkBAAICyGVvfTbaJcRHp-Ty_7tCUhlJyC5vAAIcQQAC2GN5S4YdlBixDj3AMwQ',
    'document_id1': 'BQACAgIAAxkBAAICyWVvfZLu5nQ-YQZbTcuJE7XVgDguAAIeQQAC2GN5S9CbxjREp9nSMwQ',
    'document_id2': 'BQACAgIAAxkBAAICymVvfZ79llGZS6Ormn8_CLDCcZs6AAIfQQAC2GN5S31INSkNX_pHMwQ',
    'video_id1': 'BAACAgIAAxkBAAICy2VvfbB_YwWCvE8oJWDlEdd4MUyhAAIhQQAC2GN5Sxn7lk7msLkxMwQ',
    'video_id2': 'AwACAgIAAxkBAAICzmVvfbie8f33DIPD3dbU3SGUXQiOAAIkQQAC2GN5S5ca-nyr8bhWMwQ',
}


# Функция для генерации клавиатур с инлайн-кнопками
def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    markup = get_markup(2, 'photo')
    await message.answer_photo(
        photo=LEXICON['photo_id1'],
        caption='Это фото 1',
        reply_markup=markup
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
@dp.callback_query(F.data.in_(
    ['text', 'audio', 'video', 'document', 'photo', 'voice']
))
async def process_button_press(callback: CallbackQuery, bot: Bot):
    markup = get_markup(2, 'photo')
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=LEXICON['photo_id2'],
                caption='Это фото 2'
            ),
            reply_markup=markup
        )
    except TelegramBadRequest:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=LEXICON['photo_id1'],
                caption='Это фото 1'
            ),
            reply_markup=markup
        )


# Этот хэндлер будет срабатывать на все остальные сообщения
@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Не понимаю')


if __name__ == '__main__':
    dp.run_polling(bot)