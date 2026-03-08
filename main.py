import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiohttp import web

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from oxfordLookup import getDefinitions
from googletrans import Translator

translator = Translator()
load_dotenv()

TOKEN = getenv("BOT_TOKEN")
WEBHOOK_HOST = getenv("WEBHOOK_HOST")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
PORT = int(getenv("PORT", 8000))

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("Hello, I'm Speak English bot! Send me any english words.")


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
            await message.reply(f"{word_id} - bunday so'z topilmadi")


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set: {WEBHOOK_URL}")


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    logging.info("Webhook deleted")


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    async def index(request):
        return web.Response(text="Speak English Bot ishlayapti! 🤖")

    app.router.add_get("/", index)

    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()