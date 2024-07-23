#!/usr/bin/python
# -*- coding: UTF-8 -*-
from io import BytesIO
import os
import sys
import time
import logging
import socket
from datetime import datetime

import requests
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont, ImageOps
import psutil
import RPi.GPIO as GPIO

sys.path.append("..")
from hardware.lcdlib import LCD_1inch9

logging.basicConfig(level=logging.DEBUG)

class DisplayManager:
    def __init__(self, spi_freq=10000000):
        self.rst = 27
        self.dc = 25
        self.bl = 18
        self.bus = 0
        self.device = 0
        self.fan = 37
        self.spi_freq = spi_freq

        self.disp = LCD_1inch9.LCD_1inch9(spi=SPI.SpiDev(self.bus, self.device), spi_freq=spi_freq, rst=self.rst, dc=self.dc, bl=self.bl)
        self.disp.Init()
        self.disp.clear()
        self.disp.bl_DutyCycle(50)

        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 100)
        self.font1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
        
        self.img1 = requests.get("https://raw.githubusercontent.com/itsvenox/venoLive/main/src/bot/veno_mood_1.jpg")
        self.img2 = requests.get("https://raw.githubusercontent.com/itsvenox/venoLive/main/src/bot/veno_mood_2.jpg")
        self.img5 = requests.get("https://raw.githubusercontent.com/itsvenox/venoLive/main/src/bot/veno_mood_5.jpg")
        # img1 = Image.open(BytesIO(img1.content)

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.254.254.254', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_cpu_temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = f.read()
        return float(temp) / 1000

    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def discord_bot_running(self, is_running=False):
        self.update_display(is_running)
        return is_running

    def draw_rotated_text(self, image, text, position, font, fill, angle):
        text_image = Image.new('RGBA', (image.width, image.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_image)
        draw.text((0, 0), text, font=font, fill=fill)
        rotated_text = text_image.rotate(angle, expand=1)
        x, y = position
        image.paste(rotated_text, (x, y), rotated_text)
        return image

    def display_startup_image(self):
        image = Image.open(BytesIO(self.img1.content)).convert('RGBA')
        self.disp.ShowImage(image)
        time.sleep(5)

    def turn_on_fan(self):
        cpu_temp = self.get_cpu_temp()
        if cpu_temp > 45:
            # Turn on the fan (assuming GPIO 37 is connected to the fan)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.fan, GPIO.OUT)
            GPIO.output(self.fan, GPIO.HIGH)
            logging.info("Fan turned on due to high CPU temperature")
        else:
            logging.info("CPU temperature is within safe range, fan is off")

    def update_display(self, is_running):
        current_time = datetime.now().strftime('%Y-%m-%d   %H:%M')
        ip_address = self.get_ip_address()
        cpu_temp = self.get_cpu_temp()
        cpu_usage = self.get_cpu_usage()
        
        dis_bot_status = 'ON' if is_running else 'OFF'
        tel_bot_status = 'OFF'
        self.turn_on_fan()
        if cpu_temp > 50:
            image = Image.open(BytesIO(self.img1.content)).convert('RGBA')
            # image = image.rotate(180)
            
            image = self.draw_rotated_text(image, f'{current_time}', (10, 920), self.font, (255, 255, 255), 90)
            image = self.draw_rotated_text(image, f'{ip_address}', (200, -150), self.font, (255, 255, 255), 90)
            image = self.draw_rotated_text(image, f'{cpu_temp:.1f} C       {cpu_usage:.1f}%', (960, -130), self.font, (255, 255, 255), 90)
            image = self.draw_rotated_text(image, f'{dis_bot_status}', (820, -220), self.font1, (0, 255, 0) if dis_bot_status == 'ON' else (255, 0, 0), 90)
            image = self.draw_rotated_text(image, f'{tel_bot_status}', (820, -600), self.font1, (0, 255, 0) if tel_bot_status == 'ON' else (255, 0, 0), 90)

            self.disp.ShowImage(image)
        else:
            image = Image.open(BytesIO(self.img2.content)).convert('RGBA')
            # image = image.rotate(180)
            
            image = self.draw_rotated_text(image, f'{current_time}', (10, 920), self.font, (255, 255, 255), 90)
            image = self.draw_rotated_text(image, f'{ip_address}', (200, -150), self.font, (255, 255, 255), 90)
            image = self.draw_rotated_text(image, f'{cpu_temp:.1f} C       {cpu_usage:.1f}%', (960, -130), self.font, (255, 255, 255), 90)
            image = self.draw_rotated_text(image, f'{dis_bot_status}', (820, -220), self.font1, (0, 255, 0) if dis_bot_status == 'ON' else (255, 0, 0), 90)
            image = self.draw_rotated_text(image, f'{tel_bot_status}', (820, -600), self.font1, (0, 255, 0) if tel_bot_status == 'ON' else (255, 0, 0), 90)
            self.disp.ShowImage(image)

