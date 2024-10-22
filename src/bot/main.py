import discord
from discord.ext import commands, tasks
import psutil
import socket
import subprocess
import datetime
import sys
import os
import platform

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware.lcd.display import DisplayManager

display_manager = DisplayManager()
display_manager.display_startup_image()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

# Variable to store the last command used
last_command = None

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    discord_bot_running.start()
    check_fan.start()

@bot.event
async def on_command(ctx):
    global last_command
    last_command = ctx.command.name  # Store the name of the last command

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

@bot.command(name='devices')
async def get_connected_devices(ctx):
    try:
        # Detect platform
        if platform.system() == 'Windows':
            arp_command = ['arp', '-a']
        else:
            arp_command = ['arp', '-a']

        # Run the arp command to get devices on the network
        arp_output = subprocess.check_output(arp_command).decode('utf-8')
        
        device_list = []
        for line in arp_output.splitlines():
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    ip_address = parts[1].strip('()')
                    mac_address = parts[3] if len(parts) > 3 else 'N/A'
                    
                    try:
                        # Try to get the hostname for the IP address
                        hostname = socket.gethostbyaddr(ip_address)[0]
                    except socket.herror:
                        hostname = 'Unknown'
                    
                    # Display only the last four characters of the IP address
                    device_list.append(f'IP: {ip_address[-4:]} - Hostname: {hostname}')
        
        if not device_list:
            await ctx.reply('No devices found on the network.')
        else:
            device_details = '\n'.join(device_list)
            embed = discord.Embed(title='Connected Devices', description=device_details, color=0x00ff00)
            await ctx.reply(embed=embed)
    except subprocess.CalledProcessError as e:
        await ctx.reply(f'Error executing arp command: {e}')
    except Exception as e:
        await ctx.reply(f'Error retrieving devices: {e}')


@tasks.loop(seconds=3)  # Update display every 1 seconds
async def discord_bot_running():
    display_manager.discord_bot_running(True, last_command)

@tasks.loop(seconds=30)  # Update display every 1 seconds
async def check_fan():
    display_manager.turn_on_fan()

bot.run(DISCORD_BOT_TOKEN)
