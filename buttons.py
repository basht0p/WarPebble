import time
import logger
from machine import Pin, I2C
import oled
import menu

DEBOUNCE_TIME = 900

b1_last_interrupt = 0
b2_last_interrupt = 0
bs_last_interrupt = 0
bb_last_interrupt = 0
wifi_bb_last_interrupt = 0

active_network_slide = 0

# Setup buttons
button_2 = Pin(5, Pin.IN, Pin.PULL_UP)
logger.write("Button 2 set to GPIO5, high.")

button_1 = Pin(0, Pin.IN, Pin.PULL_UP)
logger.write("Button 1 set to GPIO0, high.")

button_select = Pin(13, Pin.IN, Pin.PULL_UP)
logger.write("Select Button set to GPIO13, high.")

button_back = Pin(4, Pin.IN, Pin.PULL_UP)
logger.write("Back Button set to GPIO4, high.")

def wifi_info_button_2(pin):
    global b2_last_interrupt, active_network_slide
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, b2_last_interrupt) > DEBOUNCE_TIME:
        logger.write("wifi_info: Button 2 triggered.")
        b2_last_interrupt = current_time
        if active_network_slide == 4:
            active_network_slide = 0
        else:
            active_network_slide = active_network_slide + 1
        oled.network_slideshow(active_network_slide)

def wifi_info_button_1(pin):
    global b1_last_interrupt, active_network_slide
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, b1_last_interrupt) > DEBOUNCE_TIME:
        logger.write("wifi_info: Button 1 triggered.")
        b1_last_interrupt = current_time
        if active_network_slide == 0:
            active_network_slide = 4
        else:
            active_network_slide = active_network_slide - 1
        oled.network_slideshow(active_network_slide)

def wifi_info_back_button(pin):
    global wifi_bb_last_interrupt
    now = time.ticks_ms()
    if time.ticks_diff(now, wifi_bb_last_interrupt) > DEBOUNCE_TIME:
        logger.write("wifi_info: Back Button triggered.")
        wifi_bb_last_interrupt = now
        oled.change_view('main_menu')

def dummy_button(pin):
    logger.write("Dummy button triggered on pin " + str(pin))
        
def main_menu_button_2(pin):
    global b2_last_interrupt
    now = time.ticks_ms()
    if time.ticks_diff(now, b2_last_interrupt) > DEBOUNCE_TIME:
        logger.write("main_menu: Button 2 triggered.")
        b2_last_interrupt = now
        menu.select_tile_next(2, menu.config)

def main_menu_button_1(pin):
    global b1_last_interrupt
    now = time.ticks_ms()
    if time.ticks_diff(now, b1_last_interrupt) > DEBOUNCE_TIME:
        logger.write("main_menu: Button 1 triggered.")
        b1_last_interrupt = now
        menu.select_tile_previous(2, menu.config)
        
def main_menu_select(pin):
    global bs_last_interrupt
    now = time.ticks_ms()
    if time.ticks_diff(now, bs_last_interrupt) > DEBOUNCE_TIME:
        logger.write("main_menu: Select Button triggered.")
        bs_last_interrupt = now
        if menu.current_tile == 1:
            oled.change_view('wifi_info')
            
def change_interrupts(view='main_menu'):
    if view == 'main_menu':
        button_1.irq(
            trigger=Pin.IRQ_FALLING,
            handler=main_menu_button_1)
        logger.write("main_menu: Button 1 interrupt registered.")
        button_2.irq(
            trigger=Pin.IRQ_FALLING,
            handler=main_menu_button_2)
        logger.write("main_menu: Button 2 interrupt registered.")
        button_back.irq(
            trigger=Pin.IRQ_FALLING,
            handler=dummy_button)
        logger.write("main_menu: Dummy Button interrupt registered.")
        button_select.irq(
            trigger=Pin.IRQ_FALLING,
            handler=main_menu_select)
        logger.write("main_menu: Select Button interrupt registered.")
        
    if view == 'wifi_info':
        button_1.irq(
            trigger=Pin.IRQ_FALLING,
            handler=wifi_info_button_1)
        logger.write("wifi_info: Button 1 interrupt registered.")
        button_2.irq(
            trigger=Pin.IRQ_FALLING,
            handler=wifi_info_button_2)
        logger.write("wifi_info: Button 2 interrupt registered.")
        button_back.irq(
            trigger=Pin.IRQ_FALLING,
            handler=wifi_info_back_button)
        logger.write("wifi_info: Back Button interrupt registered.")
        button_select.irq(
            trigger=Pin.IRQ_FALLING,
            handler=dummy_button)
        logger.write("wifi_info: Dummy Button interrupt registered.")