import subprocess
import time
import sys
import gpsd
from utils.logo import v, reset, r

GPS_DEV_PATH = "/dev/ttyACM0"


def start_gps():
    # Stop any existing gpsd instances

    try:
        subprocess.call(["sudo", "-S", "killall", "gpsd"])
        time.sleep(3)
    except Exception as e:
        print(f"{r}Error stopping gpsd: {e}{reset}")

    try:
        # Start the GPS processes and monitors
        result = subprocess.call(["sudo", "-S","gpsd", GPS_DEV_PATH, "-F", "/var/run/gpsd.sock", "-n"])
        time.sleep(3)
        # Connect to the local gpsd
        gpsd.connect()
        if result != 0:
            print(f"{r}Failed to start gpsd.{reset}")
            sys.exit(1)
        print("Starting to read data from the GPS module.\nPlease wait...")

        coordinate = []
        start_time = time.time()
        timeout = 2 * 60  # 2 minutes

        while len(coordinate) == 0 and time.time() - start_time < timeout:
            gps_data = gpsd.get_current()
            if  gps_data.mode >= 2:
                if hasattr(gps_data, 'lat') and hasattr(gps_data, 'lon'):
                    latitude = gps_data.lat
                    longitude = gps_data.lon
                    coordinate = [latitude, longitude]
                    print(coordinate)
                    break
            time.sleep(1)  # Wait a bit before checking again

        if len(coordinate) == 0:
            raise ValueError("No valid GPS data received within the time limit.")

        coord = f"{latitude},{longitude}"
        url = f"https://www.google.com/maps/search/?api=1&query={coord}"

        print(f"{v}The coordinates detected are:\nLatitude: {latitude}\nLongitude: {longitude}{reset}")
        print(f"GPS coordinates can be reached at the URL: {v}{url}{reset}")

    except Exception as e:
        print(f"{r}The GPS signal is not stable and/or reachable.\nPlease position the antenna better.{reset}")
        time.sleep(1)
        option = input("Do you want to continue without a valid GPS signal?"
                       "\nPress 1 to continue without a valid GPS signal"
                       "\nPress 2 to exit."
                       "\nPlease, enter your selection: ")

        if option == '1':
            latitude, longitude = 0.0000000, 0.0000000
            url = "https://www.google.com/maps/search/?api=1&query=0.0000000,0.0000000"
            print(f"{v}The coordinates are settled by default:\nLatitude: {latitude}\nLongitude: {longitude}{reset}")

        else:
            sys.exit(1)

    return [latitude, longitude, url]
