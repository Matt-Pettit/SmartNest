import bluey
import time
import os
import subprocess

smartnest_process = None
hotspot_enabled = False
hotspot_uuid = None

def start_hotspot():
    global hotspot_enabled, hotspot_uuid

    if not hotspot_enabled:
        # Run command to start the hotspot
        cmd = "sudo nmcli device wifi hotspot ssid SmartNest password SmartNest ifname wlan0"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if "successfully activated with" in line:
                    hotspot_uuid = line.split("'")[3]
                    print(hotspot_uuid)
                    break

            if hotspot_uuid:
                hotspot_enabled = True
                print("Hotspot started")
            else:
                print("Failed to start hotspot")
        else:
            print(f"Error starting hotspot: {result.stderr}")

def stop_hotspot():
    global hotspot_enabled, hotspot_uuid

    if hotspot_enabled and hotspot_uuid:
        # Run command to stop the hotspot
        cmd = f"sudo nmcli connection down {hotspot_uuid}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            hotspot_enabled = False
            hotspot_uuid = None
            print("Hotspot stopped")
        else:
            print(f"Error stopping hotspot: {result.stderr}")

def start_smartnest():
    global smartnest_process
    if smartnest_process is None:
        smartnest_process = subprocess.Popen(["python3", "smartnest.py"])
        print("smartnest.py started")

def stop_smartnest():
    global smartnest_process
    if smartnest_process is not None:
        smartnest_process.terminate()
        smartnest_process = None
        print("smartnest.py stopped")

no_device_timer = 0

while True:
    print("Beginning New Round Of Scanning")
    nearby_devices = bluey.get_nearby_devices()
    saved_devices = bluey.read_data_file()
    device_detected = False

    for item in saved_devices:
        if item in nearby_devices:
            device_detected = True
            print("Detected Recognized Device")
            start_hotspot()
            start_smartnest()
            no_device_timer = 0
            break

    if not device_detected:
        print("No Recognized Devices")
        no_device_timer += 30
        if no_device_timer >= 600:  # 10 minutes (600 seconds)
            stop_hotspot()
            stop_smartnest()
            no_device_timer = 0

    time.sleep(60)