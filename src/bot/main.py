import os
import discord
from discord.ext import commands
# import sqlite3
# from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.all()

# Pass intents to the Bot class
bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='auh')
async def save_memory(ctx):
    await ctx.reply('YES!')

@bot.command(name='memo')
async def get_memories(ctx):
    pass


@bot.command(name='delete')
async def delete_memory(ctx):
    pass

bot.run(DISCORD_BOT_TOKEN)
