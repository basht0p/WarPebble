import time
import oled
import logger
import gc
from machine import Pin

led = Pin(15, Pin.OUT)

def toggle_led(state=0):
    if state:
        logger.write("Toggling LED.")
        if led.value():
            return
        else:
            led.value(1)
            return
    else:
        logger.write("Setting LED OFF")
        if not led.value():
            return
        else:
            led.value(0)
            return
    
wifi_connected = [[0,5,1], [1,4,1], [2,3,1], [3,2,1], [4,2,1], [5,2,1], [6,2,1], [7,2,1], [8,2,1], [9,3,1], [10,4,1], [11,5,1], [1,7,1], [2,6,1], [3,5,1], [4,4,1], [5,4,1], [6,4,1], [7,4,1], [8,5,1], [9,6,1], [10,7,1], [3,8,1], [4,7,1], [5,6,1], [6,6,1], [7,7,1], [8,8,1], [5,9,1], [6,9,1], [5,10,1], [6,10,1]]
wifi_disconnected = [[10,1,1], [3,2,1], [4,2,1], [5,2,1], [6,2,1], [9,2,1], [2,3,1], [8,3,1], [1,4,1], [4,4,1], [7,4,1], [10,4,1], [0,5,1], [3,5,1], [6,5,1], [11,5,1], [2,6,1], [5,6,1], [9,6,1], [1,7,1], [4,7,1], [7,7,1], [10,7,1], [3,8,1], [8,8,1], [2,9,1], [5,9,1], [6,9,1], [1,10,1], [5,10,1], [6,10,1]]
wifi_info_tile = [[7,6],[8,6],[9,6],[10,6],[11,6],[12,6],[13,6],[14,6],[5,7],[6,7],[7,7],[8,7],[9,7],[10,7],[11,7],[12,7],[13,7],[14,7],[15,7],[16,7],[4,8],[5,8],[6,8],[7,8],[12,8],[13,8],[14,8],[15,8],[16,8],[17,8],[18,8],[3,9],[4,9],[5,9],[11,9],[12,9],[18,9],[19,9],[2,10],[3,10],[7,10],[8,10],[9,10],[10,10],[11,10],[14,10],[15,10],[16,10],[19,10],[20,10],[1,11],[2,11],[5,11],[6,11],[7,11],[8,11],[9,11],[10,11],[14,11],[15,11],[16,11],[20,11],[1,12],[4,12],[5,12],[6,12],[10,12],[20,12],[3,13],[4,13],[8,13],[9,13],[10,13],[14,13],[15,13],[16,13],[20,13],[3,14],[6,14],[7,14],[8,14],[9,14],[10,14],[14,14],[15,14],[16,14],[20,14],[5,15],[6,15],[7,15],[10,15],[14,15],[15,15],[16,15],[20,15],[5,16],[8,16],[9,16],[10,16],[11,16],[14,16],[15,16],[16,16],[19,16],[20,16],[7,17],[8,17],[9,17],[11,17],[12,17],[18,17],[19,17],[7,18],[12,18],[13,18],[14,18],[15,18],[16,18],[17,18],[18,18],[19,18],[20,18],[10,19],[11,19],[19,19],[20,19],[21,19],[9,20],[10,20],[11,20],[12,20],[20,20],[21,20],[22,20],[9,21],[10,21],[11,21],[12,21],[21,21],[22,21],[23,21],[10,22],[11,22],[22,22],[23,22],[24,22],[23,23],[24,23]]
wardriving_tile = [[0, 0, 0, 0], [8, 0, 4, 0], [24, 0, 6, 0], [56, 0, 7, 0],
[56, 0, 7, 0], [60, 127, 143, 0], [63, 255, 255, 0], [63, 255, 255, 0], [31, 255, 254, 0],
[15, 255, 252, 0], [28, 127, 142, 0], [27, 191, 118, 0], [63, 222, 255, 0], [60, 237, 207, 0],
[60, 191, 79, 0], [62, 255, 223, 0], [63, 30, 63, 0], [55, 255, 251, 0], [51, 255, 243, 0],
[57, 255, 247, 0], [29, 127, 174, 0], [30, 33, 30, 0], [15, 128, 124, 0], [7, 204, 248, 0],
[3, 255, 240, 0], [1, 255, 224, 0], [0, 127, 128, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

def show_wifi_connected():
    if led.value():
        return
    logger.write("Drawing wifi_connected sprite.")
    oled.display.fill_rect(0, 0, 12, 12, 0)
    for pix in wifi_connected:
        oled.display.pixel(pix[0], pix[1], pix[2])
    toggle_led(1)
    oled.display.show()

def show_wifi_info_tile(x_anchor, y_anchor):
    logger.write("Drawing wifi_info tile sprite.")
    for pix in wifi_info_tile:
        oled.display.pixel(pix[0] + x_anchor, pix[1] + y_anchor, 1)
        gc.collect()
    oled.display.show()
    
def show_wardriving_tile(x_anchor, y_anchor):
    logger.write("Drawing wardriving tile sprite.")

    for y, row in enumerate(wardriving_tile):
        for x in range(26):
            byte_index = x // 8
            bit_index = 7 - (x % 8)
            if row[byte_index] & (1 << bit_index):
                oled.display.pixel(x + x_anchor, y + y_anchor, 1)

def show_wifi_disconnected():
    if not led.value():
        return
    logger.write("Drawing wifi_disconnected sprite.")
    oled.display.fill_rect(0, 0, 12, 12, 0)
    for pix in wifi_disconnected:
        oled.display.pixel(pix[0], pix[1], pix[2])
    toggle_led(0)
    oled.display.show()

def show_wifi_scanning():
    logger.write("Drawing wifi_scanning sprite.")
    oled.display.fill_rect(0, 0, 12, 12, 0)
    toggle_led(0)
    for _ in range(0, 5):
        for pix in wifi_connected:
            oled.display.pixel(pix[0], pix[1], pix[2])
        oled.display.show()
        time.sleep(0.25)
        oled.display.fill_rect(0, 0, 12, 12, 0)
        oled.display.show()
        time.sleep(0.25)
