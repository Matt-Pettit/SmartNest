import subprocess
import csv
import time

def get_nearby_devices():
    """
    Returns a list of dictionaries containing nearby Bluetooth devices.
    Each dictionary has keys 'mac' and 'name' representing the device's MAC address and name.
    """
    try:
        subprocess.run(["rfkill", "unblock", "bluetooth"])
        print("Bluetooth turned on")
    except subprocess.CalledProcessError:
        print("Failed to turn on Bluetooth")
        return []

    try:
        time.sleep(4)
        scan_output = subprocess.check_output(["hcitool", "scan"]).decode("utf-8")
    except subprocess.CalledProcessError:
        print("Failed to scan for devices")
        return []

    devices = []
    lines = scan_output.split("\n")
    for line in lines:
        if line.startswith("\t"):
            parts = line.split("\t")
            if len(parts) == 3:
                mac, name = parts[1], parts[2]
                devices.append({"mac": mac, "name": name})

    try:
        subprocess.run(["rfkill", "block", "bluetooth"])
        print("Bluetooth turned off")
    except subprocess.CalledProcessError:
        print("Failed to turn off Bluetooth")

    return devices

def read_data_file():
    """
    Reads the saved_devices.txt file and returns a list of dictionaries containing the data.
    """
    devices = []
    try:
        with open("saved_devices.txt", "r") as file:
            reader = csv.DictReader(file)
            devices = list(reader)
    except FileNotFoundError:
        pass

    return devices

def write_data_to_file(devices):
    """
    Writes the list of devices to the saved_devices.txt file, updating duplicate entries.
    """
    existing_devices = read_data_file()

    for device in devices:
        for existing in existing_devices:
            if device["mac"] == existing["mac"]:
                if existing["name"] == "n/a" and device["name"] != "n/a":
                    existing["name"] = device["name"]
                break
        else:
            existing_devices.append(device)

    try:
        with open("saved_devices.txt", "w", newline="") as file:
            fieldnames = ["mac", "name"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_devices)
        print("Nearby devices written to saved_devices.txt")
    except Exception as e:
        print(f"Failed to write to file: {e}")

def main():
    """
    Main function that calls the other functions.
    """
    nearby_devices = get_nearby_devices()
    print(nearby_devices)
    #write_data_to_file(nearby_devices)
    print(read_data_file())

if __name__ == "__main__":
    main()