import subprocess
import wifi
from utils.logo import v, reset, r
def scan_wifi ():
    wifilist = [[]]
    try:
        subprocess.call(["sudo", "systemctl", "start", "NetworkManager"])
    except:
        pass
    while len (wifilist[0])==0 or (wifilist[0])== None:
        wifilist = [[cell.ssid for cell in wifi.Cell.all('wlan0')],
                    [cell.quality for cell in wifi.Cell.all('wlan0')],
                    [cell.encryption_type for cell in wifi.Cell.all('wlan0')],
                    [cell.channel for cell in wifi.Cell.all('wlan0')],
                    [cell.address for cell in wifi.Cell.all('wlan0')],
                    [cell.mode for cell in wifi.Cell.all('wlan0')]]
    print (v,"\n\t\t\t\tNumber of networks found:",len (wifilist[0]), reset)
    print ("----------------------------------------------------------------------------------------------------------------")
    print ("---------------------------------WIFI NETWORKS AVAILABLE--------------------------------------------------------")
    print (" SSID\t\t\tQUALITY\tENCRYPTION\tCHANNEL\t\tADDRESS\t\t\tMODE\'")
    for i in range (len(wifilist[0])):
        print(r, wifilist[0][i], "\t\t\t"+str(wifilist[1][i]), "\t\t"+str(wifilist[2][i]), "\t\t"+str(wifilist[3][i]), "\t\t"+str(wifilist[4][i]), "\t\t"+str(wifilist[5][i]) ,reset)

    return (wifilist)
