#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lcdlib import LCD_1inch9
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0

logging.basicConfig(level=logging.DEBUG)

# Initialize the display with hardware SPI:
disp = LCD_1inch9.LCD_1inch9(spi=SPI.SpiDev(bus, device), spi_freq=10000000, rst=RST, dc=DC, bl=BL)

# Initialize library.
disp.Init()
# Clear display.
disp.clear()
# Set the backlight to 50% duty cycle
disp.bl_DutyCycle(50)

# Load fonts
Font1 = ImageFont.truetype("../Font/Font00.ttf", 20)
Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)

time.sleep(2)

logging.info("Showing image")

# Load the image
image1 = Image.open('../pic/veno_mood_1.jpg')
width, height = image1.size

# Create a new image with transparent background
image2 = Image.new('RGBA', (width, height), (255, 0, 0, 0))
draw2 = ImageDraw.Draw(image2)

# Define text and its properties
text = 'Hello world'
text_position = (5, 200)
text_color = (0, 255, 0, 255)  # GREEN color with full opacity in RGBA
draw2.text(text_position, text, fill=text_color, font=Font1)

# Rotate the new image
image2 = image2.rotate(-90, expand=True)

# Convert image2 to RGB mode
image2 = image2.convert('RGB')

# Define the position for pasting
px, py = 10, 10

# Paste the text image onto the original image
image1.paste(im=image2, box=(px, py), mask=image2.convert('L'))  # Use the alpha channel from image2 as mask

# Show the image on the display
disp.ShowImage(image1)

time.sleep(2)












import os
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lcdlib import LCD_1inch9
from PIL import Image, ImageDraw, ImageFont, ImageOps

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



def draw_rotated_text(image, font, text, angle, x, y):
    txt = Image.new(image.mode, font)
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, font=font, fill=(255, 0, 0))
    txt = txt.rotate(angle, expand=1)
    image.paste(txt, (int(x - txt.width/2), int(y - txt.height/2)), txt)


# img = Image.open('../pic/veno_mood_1.jpg')
# width, height = img.size

# # #draw = ImageDraw.Draw(img)

# font = ImageFont.truetype('Pillow/Tests/fonts/FreeSansBold.ttf', 30)
# text_layer = Image.new('L', (width, height))
# draw = ImageDraw.Draw(text_layer)
# draw.text( (30, 0), "Text rotated",  font=font, fill=255)

# rotated_text_layer = text_layer.rotate(10.0, expand=1)
# img.paste( ImageOps.colorize(rotated_text_layer, (0,0,0), (10, 10,10)), (42,60),  rotated_text_layer)

images = ['../pic/veno_mood_1.jpg', '../pic/veno_mood_2.jpg', '../pic/veno_mood_3.jpg', '../pic/veno_mood_4.jpg', '../pic/veno_mood_5.jpg']
while True:
    for i in images :
        img = Image.open(i)
        width, height = img.size
        font = ImageFont.truetype('Pillow/Tests/fonts/FreeSansBold.ttf', 30)
        disp.ShowImage(images[i])
        i = i+1
        time.sleep(3)

# draw_rotated_text(image, font, "zero", 0, image.width/2, image.height/2)