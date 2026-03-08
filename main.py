import asyncio
import logging
import sys

from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from oxfordLookup import getDefinitions
from googletrans import Translator

translator = Translator()

load_dotenv()


# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:

    await message.answer(f"Hello, I'm Speak English bot! Send me any english words.")



@dp.message()
async def google_translator(message: Message) -> None:
    detected = await translator.detect(message.text)
    lang = detected.lang
    if len(message.text.split()) > 2:
        dest = "uz" if lang == "en" else "en"
        translated = await translator.translate(message.text, dest=dest)
        await message.reply(translated.text)
    else:
        if lang == "en":
            word_id = message.text
        else:
            translated = await translator.translate(message.text, dest='en')
            word_id = translated.text
        print(word_id)
        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \n Definition: \n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
            else:
                await message.reply(f"No definition found for word {word_id}")
        else:
            await message.reply(f"{word_id} - bunday so'z topilmadi")




async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())