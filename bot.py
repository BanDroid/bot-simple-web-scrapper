__import__("dotenv").load_dotenv()

import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
from os import environ as env

from parser import BsParser
from network import http_get
from utils import send_message_as_file

BOT_TOKEN = env.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise EnvironmentError("BOT_TOKEN variable is needed!")

description = """Bot untuk web scrapping sederhana."""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="scrapper ", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready")


@bot.command(name="get")
async def scrapper_get(
    context,
    url=None,
    selector="body",
    attributes="innerHTML",
    *,
    template: str = "```html\n$1```",
):
    if not url:
        await context.reply("URL tidak boleh kosong ya...")
        return
    await context.send(f"Sedang memproses halaman...\n```yaml\nURL: {url}```")

    output_template = f" ".join(template.splitlines()[1:-1])
    error, response_str = await http_get(url)
    if error:
        await context.reply(response_str)
        return

    # TODO: parsing element
    parsed = BsParser(response_str)
    try:
        parsed.process_selector(selector, attributes.split(","))
        output_as_message = parsed.get_formatted_output(output_template)
    except Exception as error:
        if len(str(error)) >= 2000:
            await send_message_as_file(
                context=context,
                message="Hasil melebihi 2000 karakter, format akan diberikan dalam bentuk file teks.",
                file_content=error,
                user_id=context.author.id,
            )
            return
        await context.reply(f"Terdapat error.\n```bash\n{error}```")
        return
    if not output_as_message:
        await send_message_as_file(
            context=context,
            message="Hasil kosong, berikut document html:",
            file_content=parsed.document.prettify(),
            user_id=context.author.id,
        )
        return
    if len(output_as_message) >= 2000:
        await send_message_as_file(
            context=context,
            message="Hasil melebihi 2000 karakter, format akan diberikan dalam bentuk file teks.",
            file_content=output_as_message,
            user_id=context.author.id,
        )
        return
    await context.reply(output_as_message)


bot.run(BOT_TOKEN)
