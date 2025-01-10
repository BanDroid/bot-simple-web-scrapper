__import__("dotenv").load_dotenv()

import sys
import discord
from discord.ext import commands
import asyncio
from bs4 import BeautifulSoup
from os import environ as env

from parser import BsParser
from network import http_get
from utils import send_message_as_file

BOT_TOKEN = env.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise EnvironmentError("BOT_TOKEN variable is needed!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="scrapper ",
    description="""Bot for simple web scrapping.""",
    intents=intents,
)


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
    template: str = "```html\n$1\n```",
):
    if not url:
        await context.reply("URL cannot be empty!")
        return
    await context.send(f"Processing the page...\n```yaml\nURL: {url}```")

    output_template = f" ".join(template.splitlines()[1:-1])
    is_error_http, response_str = await http_get(url)
    if is_error_http:
        await send_message_as_file(
            context=context,
            message="There was unexpected error processing requests:",
            file_content=response_str,
            user_id=context.author.id,
        )
        return
    try:
        parsed = BsParser(response_str)
        parsed.process_selector(selector, attributes.split(","))
        output_as_message = parsed.get_formatted_output(output_template)
    except Exception as error:
        await send_message_as_file(
            context=context,
            message="There was unexpected error when parsing:",
            file_content=error,
            user_id=context.author.id,
        )
        return
    if not output_as_message:
        await send_message_as_file(
            context=context,
            message="Empty result, below here is the following document page:",
            file_content=parsed.document.prettify(),
            user_id=context.author.id,
        )
        return
    await send_message_as_file(
        context=context,
        message="Your request has been finished, below here is the following text document:",
        file_content=output_as_message,
        user_id=context.author.id,
    )


bot.run(BOT_TOKEN)
