from machine import Pin, I2C
import time
import logger
from wifi import station_interface
import sprites
import menu
import buttons
import ssd1306

i2c = I2C(scl=Pin(12), sda=Pin(14), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

def clear_header():
    display.fill_rect(0, 0, 128, 15, 0)
    display.show()
    logger.write("oled: Header cleared.")

def clear_title():
    display.fill_rect(24, 0, 128, 15, 0)
    display.show()
    logger.write("oled: Title cleared.")

def clear_body():
    display.fill_rect(0, 16, 128, 64, 0)
    display.show()
    logger.write("oled: Body cleared.")

def clear_display():
    display.fill(0)
    display.show()
    logger.write("oled: Display cleared.")

def show_boot_message():
    logger.write("Showing boot message.")
    display.fill(0)
    display.text("Booted", 34, 5, 1)
    display.hline(0, 15, 128, 1)
    display.text("The War Pebble", 5, 30, 1)
    display.text("ver. 1.2", 20, 51, 4)
    display.show()
    sprites.toggle_led(1)
    time.sleep(1)
    sprites.toggle_led(0)
    clear_body()
    clear_header()

def network_slideshow(slide=0):
    logger.write("wifi_info: Drawing wifi info slide " + str(slide) + ".")
    
    clear_body()
    
    if_config = station_interface.ifconfig()
    
    details = [
        ( "SSID", str(station_interface.config('ssid')) ),
        ( "IPv4 Address", if_config[0] ),
        ( "Subnet Mask", if_config[1] ),
        ( "Gateway", if_config[2] ),
        ( "DNS Server", if_config[3] ),
    ]

    current_slide_details = details[slide]
    clear_title()
    display.text(current_slide_details[0], 24, 3, 1)
    display.text(current_slide_details[1], 12, 36, 1)
        
    display.show()
    
def change_view(view='main_menu'):
    if view == 'wifi_info':
        logger.write("Setting wifi_info view.")
        clear_body()
        clear_title()
        network_slideshow()
        buttons.change_interrupts('wifi_info')
    
    if view == 'main_menu':
        logger.write("Setting main_menu view.")
        clear_body()
        clear_title()
        menu.tile(0, 1, **menu.config)
        menu.tile(1, 2, **menu.config)
        buttons.change_interrupts('main_menu')
        display.text(menu.items['1'], 32, 3, 1)
        display.show()