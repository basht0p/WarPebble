import time
import menu
import logger
import oled
import sprites
import wifi
logger.write("Libraries imported successfully!")

oled.show_boot_message()

oled.change_view('main_menu')

while True:
    
    # Check Wifi
    if wifi.station_interface.isconnected():
        sprites.show_wifi_connected()
    else:
        sprites.show_wifi_disconnected()
        wifi.parasitic_wifi()
    time.sleep(0.1)