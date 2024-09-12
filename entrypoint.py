from  utils.gps_manager import start_gps
from  utils.wifi_monitor import scan_wifi



def main():

    #     Starting gps coordinate search
    coordinate = start_gps()

    #     Start wifi scan via less powerful wlan0 (raspberry's network card) to avoid taking other networks except our
    wifi_list = scan_wifi()




if __name__ == "__main__":
    main()
