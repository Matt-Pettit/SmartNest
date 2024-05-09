import csv
from datetime import datetime, timedelta
import random

# Define the image names
image_names = ["camera_preview_inside.png", "camera_preview_outside.png"]

# Define the start timestamp
start_timestamp = datetime(2024, 3, 3, 18, 46)

# Define the fieldnames
fieldnames = ["Timestamp", "Location", "Temperature", "Humidity", "ImageName"]

# Generate fake data
data = []
for i in range(100):
    timestamp = start_timestamp + timedelta(minutes=i)
    location = "Inside" if i % 2 == 0 else "Outside"
    temperature = random.randint(20, 50)
    humidity = random.randint(20, 80)
    image_name = random.choice(image_names)
    data.append({"Timestamp": timestamp.strftime("%Y/%m/%d %H:%M"),
                 "Location": location,
                 "Temperature": str(temperature),
                 "Humidity": str(humidity),
                 "ImageName": image_name})

# Sort the data by timestamp
data.sort(key=lambda x: x["Timestamp"])

# Open a CSV file for writing
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for row in data:
        writer.writerow(row)