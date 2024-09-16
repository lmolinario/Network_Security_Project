from  utils.gps_manager import start_gps
from  utils.wifi_monitor import scan_wifi
from utils.wifi_exploit import hack_wifi
from utils.vulnerability_finder import vuln_find


def main():

    #     Starting gps coordinate search
    coordinate = start_gps()

    #     Start wifi scan via less powerful wlan0 (raspberry's network card) to avoid taking other networks except our
    wifi_list = scan_wifi()

    #     Hack of wifi via wlan1 (monitor network card  "Alfa" )
    wifi_list_exploited = hack_wifi(wifi_list)

    #     Vulnerabilities scan
    wifi_list_mapped = vuln_find(wifi_list_exploited)


if __name__ == "__main__":
    main()
