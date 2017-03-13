from PIL import Image
from tinkerforge.bricklet_oled_128x64 import BrickletOLED128x64


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


def draw_image(controller, image):
    image = Image.open("images/" + str(image) + ".png")
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
    draw_matrix(controller.screen, 0, 0, 128, 8, pixels)


def screen_setup(controller, uid):
    if not controller.screen:
        controller.screen = BrickletOLED128x64(uid, controller.ipcon)
        controller.screen.clear_display()
        controller.screen.set_display_configuration(0, False)
        draw_image(controller, "splash")
