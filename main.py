# main.py

import os
import random
from urllib.parse import urlparse
from dotenv import load_dotenv
import datetime
import asyncio

import discord
from discord.ext import commands

import utils
from lilu_phrases import general_phrases
from lilunews import News


load_dotenv()




GUILD_IDS = [836679617552973934]

news = News.default()
client = discord.Bot(debug_guilds=GUILD_IDS)


@client.event
async def on_error(event, *args, **kwargs):
    with open('errors.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    utils.print_guilds(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if (not utils.is_mention_user(message, client.user)):
        return

    r = random.choices(general_phrases, k = 1)[0]
    await message.channel.send(r)


@client.slash_command(
    name='roll',
    description='Число от 1 до 100 (по умолчанию)',
    guild_ids=GUILD_IDS
)
async def roll(ctx):
    r = random.randint(1, 100)
    print(f'Rolling {r} of {100}')
    await ctx.respond(r)

@client.slash_command(
    name='новость',
    description='Каких чудес гейм дев нам приготовил. А может... АНИМЕ?!',
    guild_ids=GUILD_IDS
)
async def tell_me_news(ctx):
    item = news.get_random()

    print(f'News: {ctx.user.name} - {item[0]}')

    async with ctx.channel.typing():
        await asyncio.sleep(random.randint(5, 20) * 0.1)

    top_d = urlparse(item[2]).netloc
    d = '.'.join(top_d.split('.')[-2:])

    r = f"Новость для <@{ctx.user.id}> ({item[1]}):" #   от {d}  ```{item[0]}```
    embed = discord.Embed(description=item[0], color=discord.Colour.embed_background())
    await ctx.respond(r, embed=embed)


def main():
    client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()