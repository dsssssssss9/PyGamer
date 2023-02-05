import time, board, terminalio
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font
import displayio
import neopixel
from adafruit_cursorcontrol.cursorcontrol import Cursor
from adafruit_cursorcontrol.cursorcontrol_cursormanager import DebouncedCursorManager

# Set the NeoPixel brightness
NEO_BRIGHTNESS = 0.3

# Set up the NeoPixel strip
strip = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=NEO_BRIGHTNESS)

# Turn off NeoPixels to start
strip.fill((255,0,0))

# Create the display
display = board.DISPLAY

# Create the display context
splash = displayio.Group()

# Button colors
RED = (255, 0, 0)
ORANGE = (255, 34, 0)
YELLOW = (255, 170, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
VIOLET = (153, 0, 255)
MAGENTA = (255, 0, 51)
PINK = (255, 51, 119)
AQUA = (85, 125, 255)
WHITE = (255, 255, 255)
LIME = (102, 255, 0)
OFF = (0, 0, 0)
font_file12 = "fonts/Alice1MX-12.bdf"
font_file18 = "fonts/GoMono-Bold-18.bdf"
myfont12 = bitmap_font.load_font(font_file12)
myfont18 = bitmap_font.load_font(font_file18)

# Button properties
btn_x = 40
btn_y = 40

spots = [
    {"label": "1", "pos": (0, 5), "size": (btn_x, btn_y), "color": RED},
    {"label": "2", "pos": (40, 5), "size": (btn_x, btn_y), "color": ORANGE},
    {"label": "3", "pos": (80, 5), "size": (btn_x, btn_y), "color": YELLOW},
    {"label": "4", "pos": (120, 5), "size": (btn_x, btn_y), "color": GREEN},
    {"label": "5", "pos": (0, 45), "size": (btn_x, btn_y), "color": CYAN},
    {"label": "6", "pos": (40, 45), "size": (btn_x, btn_y), "color": BLUE},
    {"label": "7", "pos": (80, 45), "size": (btn_x, btn_y), "color": VIOLET},
    {"label": "8", "pos": (120, 45), "size": (btn_x, btn_y), "color": MAGENTA},
    {"label": "9", "pos": (0, 85), "size": (btn_x, btn_y), "color": PINK},
    {"label": "10", "pos": (40, 85), "size": (btn_x, btn_y), "color": AQUA},
    {"label": "11", "pos": (80, 85), "size": (btn_x, btn_y), "color": WHITE},
    {"label": "12", "pos": (120, 85), "size": (btn_x, btn_y), "color": OFF},
]

buttons = []
for spot in spots:
    fc=spot["color"]
    nm=spot["label"]
    ivc = ((255-fc[0])& 0b11111) << 11
    ivc += ((255-fc[1]) & 0b111111) << 5
    ivc += (255-fc[2]) & 0b11111
    print(f"{nm}: Inverse of {fc} is {hex(ivc)}")
    ivc = ((255-fc[0])& 0b11111) << 11
    ivc += ((255-fc[1]) & 0b111111) << 5
    ivc += (255-fc[2]) & 0b11111
    
    button = Button(
        x=spot["pos"][0],
        y=spot["pos"][1],
        width=spot["size"][0],
        height=spot["size"][1],
        style=Button.SHADOWROUNDRECT,
        fill_color=spot["color"],
        #outline_color=0x222222,
        outline_color=ivc,
        name=spot["label"],
        label_font=myfont18,
        label=spot["label"],
        label_color=ivc,
    )
    splash.append(button)
    buttons.append(button)

# initialize the mouse cursor object
mouse_cursor = Cursor(display, display_group=splash)

# initialize the cursormanager
cursor = DebouncedCursorManager(mouse_cursor)

# Show splash group
display.show(splash)

prev_btn = None
while True:
    cursor.update()
    if cursor.is_clicked is True:
        for i, b in enumerate(buttons):
            if b.contains((mouse_cursor.x, mouse_cursor.y)):
                b.selected = True
                print("Button %d clicked" % i)
                strip.fill(b.fill_color)
                prev_btn = b
    elif prev_btn is not None:
        prev_btn.selected = False
    time.sleep(0.1)
