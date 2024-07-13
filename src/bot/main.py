import os
import discord
from discord.ext import commands
import psutil
import socket
# from dotenv import load_dotenv
# load_dotenv()


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='WEE')
async def wee(ctx):
    await ctx.reply('WEEEEE!')


@bot.command(name='status')
async def get_status(ctx):
    # Get CPU temperature
    temp = psutil.sensors_temperatures()['cpu_thermal'][0].current

    # Get IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

    # Send message with hardware information
    await ctx.reply(f'CPU Temperature: {temp}°C\nIP Address: {ip_address}')



@bot.command(name='delete')
async def delete_memory(ctx):
    pass


bot.run(DISCORD_BOT_TOKEN)
