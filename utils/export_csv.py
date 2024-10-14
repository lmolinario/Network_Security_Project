import csv
import os
from datetime import datetime


def export_csv(coordinate, listawifi):
    url = coordinate[2]
    latitude = coordinate[0]
    longitude = coordinate[1]

    wifi_counter = len(listawifi[0])

    date = datetime.now().strftime("%d/%m/%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    ssid = listawifi[0]
    quality = listawifi[1]
    encryption_type = listawifi[2]
    channel = listawifi[3]
    address = listawifi[4]
    mode = listawifi[5]
    password = listawifi[6]
    ip = listawifi[7]
    vuln = listawifi[8]

    file_exists = os.path.isfile("wifi.csv")

    if not file_exists:
        print("There is no 'wifi.csv' file to export the data to.")
        print("I'll try to generate it.\nPlease wait...")
    else:
        print(
            "There is already a 'wifi.csv' file to which to export the data.\nI will append the data.\nPlease wait...")

    try:
        with open('wifi.csv', 'a', newline='') as csvfile:
            fieldnames = ["Date", "Time", 'Latitude', 'Longitude', 'SSID', 'Quality', "Encryption", "Channel",
                          "Address", "Mode", "Password", "Ip", "Vulnerability", "URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            i = 0
            while i < wifi_counter and len (ip) ==wifi_counter:
                writer.writerow(
                    {"Date": date, "Time": current_time, 'Latitude': latitude, 'Longitude': longitude, 'SSID': ssid[i],
                     'Quality': quality[i], "Encryption": encryption_type[i], "Channel": channel[i],
                     "Address": address[i], "Mode": mode[i], "Password": password[i],
                     "Ip": ip[i], "Vulnerability": vuln[i], "URL": url})
                i = i + 1
        print("Data export to 'wifi.csv' file was successful")
    except Exception as e:
        print(f"An error occurred: {e}")

    return listawifi
