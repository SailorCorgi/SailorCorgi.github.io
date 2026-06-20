#Example of how to parse .lcd files 
#based on how im doing it in project on a esp32
from machine import Pin, I2C
from i2c_lcd import LCD_I2C
import time

# I2C
i2c = I2C(1, scl=Pin(9), sda=Pin(8), freq=400000)

print("I2C devices:", [hex(x) for x in i2c.scan()])

# 20x4 LCD at 0x27
lcd = LCD_I2C(i2c, 0x27, 4, 20)


def load_lcd_art(filename):
    """Load .lcd file exported by the LCD Art-to-Text tool"""

    custom_chars = []
    grid_rows = []
    current_bitmap = []
    mode = None

    with open(filename, "r") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith("#"):
                if "GRID" in line:
                    mode = "grid"
                elif "CUSTOM CHARS" in line or "LCD ART EXPORT" in line:
                    mode = "chars"
                continue

            if mode == "chars" and line.startswith("B"):
                current_bitmap.append(int(line[1:], 2))

                if len(current_bitmap) == 8:
                    custom_chars.append(current_bitmap)
                    current_bitmap = []

            elif mode == "grid":
                grid_rows.append([int(tok) for tok in line.split()])

    if len(custom_chars) > 8:
        custom_chars = custom_chars[:8]

    return custom_chars, grid_rows


def show_lcd_art(filename):
    custom_chars, grid_rows = load_lcd_art(filename)

    # Load custom chars into CGRAM
    for slot in range(len(custom_chars)):
        lcd.custom_char(slot, custom_chars[slot])

    lcd.clear()

    # Draw grid
    for row_index, row in enumerate(grid_rows):
        lcd.set_cursor(0, row_index)

        for code in row:
            if code < 8:
                lcd.print_custom_char(code)
            else:
                lcd.print(chr(code))


# Example usage

show_lcd_art("cheesin.lcd")
time.sleep(3)

show_lcd_art("teeth.lcd")
time.sleep(3)

show_lcd_art("smile.lcd")
