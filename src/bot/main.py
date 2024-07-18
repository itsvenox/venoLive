
import discord
from discord.ext import commands
import psutil
import socket
import subprocess
import datetime
import sys
import os



# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lcd.example.display import DisplayManager

display_manager = DisplayManager()
display_manager.display_startup_image()



intents = discord.Intents.all()


bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    display_manager.is_discord_bot_running(True)


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

    # Get WiFi information
    wifi_info = subprocess.check_output(['iwconfig']).decode('utf-8')
    wifi_ssid = None
    wifi_signal = None
    for line in wifi_info.split('\n'):
        if 'ESSID' in line:
            wifi_ssid = line.split(':')[1].strip().replace('"', '')
        elif 'Link Quality' in line:
            wifi_signal = line.split('=')[1].strip()

    # Get current time
    current_time = datetime.datetime.now().strftime('%d/%m/%Y - %H:%M')

    # Create an embed with the hardware information
    embed = discord.Embed(title='System Status', color=0x00ff00)
    embed.add_field(name='Current Time : ', value=current_time, inline=True)
    embed.add_field(name='CPU Temperature : ', value=f'{temp}°C', inline=True)
    embed.add_field(name='IP Address : ', value=ip_address, inline=True)
    embed.add_field(name='WiFi SSID : ', value=wifi_ssid, inline=True)
    embed.add_field(name='WiFi Signal : ', value=wifi_signal, inline=True)

    # Send the embed
    await ctx.reply(embed=embed)

@bot.command(name='delete')
async def delete_memory(ctx):
    pass

while True:
    display_manager.update_display()

bot.run(DISCORD_BOT_TOKEN)