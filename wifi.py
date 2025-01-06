import network
import logger
import sprites

station_interface = network.WLAN(network.WLAN.IF_STA)
if station_interface.active() == False:
    station_interface.active(True)

ap_interface = network.WLAN(network.WLAN.IF_AP)
if ap_interface.active():
    ap_interface.active(False)

## IDEA: "Force" parameter to force a disconnect/reconnect

def parasitic_wifi(retrigger=0):
        if not retrigger == 0:
            station_interface.disconnect()
            time.sleep(5)
        sprites.show_wifi_scanning()
        logger.write("Scanning for wifi...")
        scan_results = station_interface.scan()
        if scan_results:
            open_ssids = [entry for entry in scan_results if entry[4] == 0]
            if open_ssids:
                logger.write("Found open SSIDs.")
                for ssid in open_ssids:
                    if station_interface.isconnected():
                        sprites.show_wifi_connected()
                        logger.write("Connected to " + ssid)
                        break
                    else:
                        sprites.show_wifi_scanning()
                        try:
                            station_interface.connect(ssid, '')
                            logger.write("Trying to connect to " + ssid + "...")
                        except OSError as e:
                            logger.write(e)
