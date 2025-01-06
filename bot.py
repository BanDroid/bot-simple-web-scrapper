__import__("dotenv").load_dotenv()

import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
from os import environ as env

from parser import BsParser
from network import http_get

BOT_TOKEN = env.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise EnvironmentError("BOT_TOKEN variable is needed!")

description = """Bot untuk web scrapping sederhana."""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready")


@bot.command(name="scrapper-get")
async def scrapper_get(
    context,
    url=None,
    selector="body",
    attributes="text",
    *template,
):
    if not url or not selector:
        await context.reply("URL tidak boleh kosong ya...")
        return
    await context.send(f"Sedang memproses halaman...\n```yaml\nURL: {url}```")

    output_template = f" ".join(template[1:-1])
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
            await context.reply(
                f"Terdapat error dan pesan error melebihi 2000 karakter, harap cek di log server."
            )
            return
        await context.reply(f"Terdapat error.\n```bash\n{error}```")
        return
    if not output_as_message:
        try:
            await context.reply(
                f"Hasil kosong, berikut document html:\n```html\n{parsed.document.body.prettify()}\n```"  # type: ignore
            )
            return
        except:
            await context.reply(
                f"Hasil kosong, dan berikut judul halaman:\n```html\n{parsed.document.title}\n```"
            )
            return
    if len(output_as_message) >= 2000:
        await context.reply(f"Hasil melebihi 2000 karakter")
        return
    await context.reply(output_as_message)


bot.run(BOT_TOKEN)
