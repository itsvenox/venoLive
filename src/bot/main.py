
import discord
from discord.ext import commands, tasks
import psutil
import socket
import subprocess
import datetime
import sys
import os



# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware.lcd.display import DisplayManager

display_manager = DisplayManager()
display_manager.display_startup_image()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    discord_bot_running.start()
    ckeck_fan.start()
    # update_display.start()  # Start the update_display task

@bot.command(name='WEE')
async def wee(ctx):
    await ctx.reply('WEEEEE!')

@bot.command(name='status')
async def get_status(ctx):
    try:
        # Get CPU temperature
        temps = psutil.sensors_temperatures()
        if 'cpu_thermal' in temps:
            temp = temps['cpu_thermal'][0].current
        else:
            temp = 'N/A'

        # Get IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()

        # Get WiFi information
        try:
            wifi_info = subprocess.check_output(['iwconfig']).decode('utf-8')
            wifi_ssid = None
            wifi_signal = None
            for line in wifi_info.split('\n'):
                if 'ESSID' in line:
                    wifi_ssid = line.split(':')[1].strip().replace('"', '')
                elif 'Link Quality' in line:
                    wifi_signal = line.split('=')[1].strip()
        except subprocess.CalledProcessError:
            wifi_ssid = 'N/A'
            wifi_signal = 'N/A'

        # Get current time
        current_time = datetime.datetime.now().strftime('%d/%m/%Y - %H:%M')

        # Create an embed with the hardware information
        embed = discord.Embed(title='System Status', color=0x00ff00)
        embed.add_field(name='Current Time', value=current_time, inline=True)
        embed.add_field(name='CPU Temperature', value=f'{temp}°C', inline=True)
        embed.add_field(name='IP Address', value=ip_address, inline=True)
        embed.add_field(name='WiFi SSID', value=wifi_ssid, inline=True)
        embed.add_field(name='WiFi Signal', value=wifi_signal, inline=True)

        # Send the embed
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(f'Error retrieving status: {e}')

@bot.command(name='delete')
async def delete_memory(ctx):
    # Implement memory delete functionality here
    pass

@tasks.loop(seconds=3)  # Update display every 1 seconds
async def discord_bot_running():
    display_manager.discord_bot_running(True)


@tasks.loop(seconds=30)  # Update display every 1 seconds
async def ckeck_fan():
    display_manager.turn_on_fan()

bot.run(DISCORD_BOT_TOKEN)