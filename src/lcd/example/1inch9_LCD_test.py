#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import logging
import socket
from datetime import datetime
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont, ImageOps
import psutil

sys.path.append("..")
from lcdlib import LCD_1inch9

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0

logging.basicConfig(level=logging.DEBUG)

# Initialize the display with hardware SPI:
disp = LCD_1inch9.LCD_1inch9(spi=SPI.SpiDev(bus, device), spi_freq=10000000, rst=RST, dc=DC, bl=BL)

disp.Init()
disp.clear()
disp.bl_DutyCycle(50)



def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = f.read()
    return float(temp) / 1000

def get_cpu_usage():
    return psutil.cpu_percent()

def draw_rotated_text(image, text, position, font, fill, angle):

    text_image = Image.new('RGBA', (image.width, image.height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text, font=font, fill=fill)
    rotated_text = text_image.rotate(angle, expand=1)
    x, y = position
    image.paste(rotated_text, (x, y), rotated_text)
    return image


while True:
    current_time = datetime.now().strftime('%Y-%m-%d   %H:%M')
    ip_address = get_ip_address()
    cpu_temp = get_cpu_temp()
    cpu_usage = get_cpu_usage()
    for i in range(1, 6):
        # Open image
        image = Image.open(f'../pic/veno_mood_{i}.jpg').convert('RGBA')
        image.rotate(180)
        # Get current time, IP address, and CPU temperature
        

        # Load font
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 100)
        font1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
        # Draw rotated text on the image
        image = draw_rotated_text(image, f'{current_time}', (10, 920), font, (255, 255, 255), 90)
        image = draw_rotated_text(image, f'{ip_address}', (200, -150), font, (255, 255, 255), 90)
        image = draw_rotated_text(image, f'{cpu_temp:.1f} C       {cpu_usage:.1f}%', (960, -130), font, (255, 255, 255), 90)
        image = draw_rotated_text(image, f'ON', (820, -220), font1, (0, 255, 0), 90)
        # Display image
        disp.ShowImage(image)

        # Pause before showing the next image
        time.sleep(3)