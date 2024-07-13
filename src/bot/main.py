import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='WEE')
async def wee(ctx):
    await ctx.reply('WEEEEE!')


@bot.command(name='memo')
async def get_memories(ctx):
    pass


@bot.command(name='delete')
async def delete_memory(ctx):
    pass


bot.run(DISCORD_BOT_TOKEN)
