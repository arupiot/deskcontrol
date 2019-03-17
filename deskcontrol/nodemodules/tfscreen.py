from classes.tfmodule import TinkerForgeModule
from PIL import Image, ImageDraw, ImageFont
from tinkerforge.bricklet_oled_128x64 import BrickletOLED128x64

FONT = 'images/Times New Roman.ttf'


def draw_matrix(scr, start_column, start_row, column_count, row_count, pixels):
    pages = []
    for row in range(row_count):
        pages.append([])

        for column in range(column_count):
            page = 0

            for bit in range(8):
                if pixels[(row * 8) + bit][column]:
                    page |= 1 << bit

            pages[row].append(page)
    data = []
    for row in range(row_count):
        for column in range(column_count):
            data.append(pages[row][column])
    scr.new_window(start_column, start_column + column_count - 1,
                   start_row, start_row + row_count - 1)
    for i in range(0, len(data), 64):
        block = data[i:i + 64]
        scr.write(block + [0] * (64 - len(block)))


class TinkerForgeScreenModule(TinkerForgeModule):
    device = None

    def __init__(self, *args, **kwargs):
        super(TinkerForgeScreenModule, self).__init__(*args, **kwargs)
        
    def draw_splash(self):
        image = Image.open("images/splash.png")
        self.process_image(image)

    def try_bricklet(self, uid, device_identifier, position):
        if not self.device:
            if device_identifier == 263:
                self.device = BrickletOLED128x64(uid, self.controller.ipcon)
                self.device.clear_display()
                self.device.set_display_configuration(0, False)
                self.draw_splash()
                print("Screen Initialised")
                return True
            return False


    def callback_sleep(self, data):
        if self.device:
            if 'sleep' in data:
                self.device.clear_display()
            if 'wake' in data:
                self.draw_splash()


    def process_image(self, image):
        if self.device:
            image = image.convert("1")
            image_data = image.load()
            pixels = []
            for row in range(64):
                pixels.append([])
                for column in range(128):
                    if column < image.size[0] and row < image.size[1]:
                        pixel = image_data[column, row] > 0
                    else:
                        pixel = False
                    pixels[row].append(pixel)
            draw_matrix(self.device, 0, 0, 128, 8, pixels)

    def draw(self, layout, params):
        if layout in ["menu", "values"]:
            image = Image.open("images/menu.png")
        else:
            image = Image.open("images/nothing.png")
        forward = Image.open("images/forward.png")
        back = Image.open("images/back.png")
        if "icon" in params:
            icon = Image.open("images/" + params["icon"] + ".png")

        if layout == "menu":
            font_t = ImageFont.truetype(FONT, 24)
            d = ImageDraw.Draw(image)
            image.paste(forward, (110, 20))
            image.paste(icon, (90, 10))
            d.text((10, 30), params["title"].title(), fill=255, font=font_t)

        elif layout == "values":
            image.paste(back, (-5, 20))

            font_t = ImageFont.truetype(FONT, 18)
            font_v = ImageFont.truetype(FONT, 20)
            d = ImageDraw.Draw(image)

            if "title" not in params:
                d.text((20, 12), "Nothing\nConnected", fill=255, font=font_t)
            else:
                d.text((15, 7), params["title"].title(), fill=255, font=font_t)
                if params["value"]:
                    d.text((20, 28), params["value"], fill=255, font=font_v)

        elif layout == "edit":
            image.paste(back, (-5, 20))

            font_t = ImageFont.truetype(FONT, 18)
            font_v = ImageFont.truetype(FONT, 20)
            d = ImageDraw.Draw(image)

            d.text((15, 7), params["title"].title(), fill=255, font=font_t)
            d.text((20, 28), params["value"], fill=255, font=font_v)

        self.process_image(image)
