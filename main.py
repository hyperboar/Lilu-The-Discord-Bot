# main.py

import os
import random
from dotenv import load_dotenv

import discord
from discord.ext import commands

import utils
from lilunews import News


load_dotenv()


LiluPhrase = 'Lilu Dallas multipass!'


TOKEN = os.getenv('DISCORD_TOKEN')
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

    await message.channel.send(LiluPhrase)


@client.slash_command(
    name='roll',
    description='Число от 1 до 100 (по умолчанию)',
    guild_ids=GUILD_IDS
)
async def roll(ctx, ):
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
    r = f"Новость для <@{ctx.user.id}>:```{item[0]}```"
    print(f'News: {item[0]}')
    await ctx.respond(r)



def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()