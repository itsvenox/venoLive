import sys
from PIL import Image
import st7789

disp = st7789.ST7789(
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


WIDTH = disp.width
HEIGHT = disp.height


def setup_ui():
    image_file = "assets/veno_mood_1.png"

    # Initialize display.
    disp.begin()

    # Load an image.
    print(f"Loading image: {image_file}...")
    image = Image.open(image_file)
    image = image.resize((WIDTH, HEIGHT))

    print("Drawing image")

    disp.display(image)