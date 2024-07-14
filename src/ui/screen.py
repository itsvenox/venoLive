import sys
from PIL import Image
import st7789


class Screen:
    def __init__(self):
        # self.width = width
        # self.height = height
        self.disp = st7789.ST7789(
            height=320,
            width=170,
            rotation=180,
            port=0,
            cs=1,
            dc=9,
            backlight=13,
            spi_speed_hz=60 * 1000 * 1000,
            offset_left=0,
            offset_top=0,
        )
        self.WIDTH = self.disp.width
        self.HEIGHT = self.disp.height


    def setup_screen(self):
        image_file = "assets/veno_mood_1.png"
        # Initialize display.
        self.disp.begin()
        # Load an image.
        print(f"Loading image: {image_file}...")
        image = Image.open(image_file)
        image = image.resize((self.WIDTH, self.HEIGHT))
        print("Drawing image")
        self.disp.display(image)