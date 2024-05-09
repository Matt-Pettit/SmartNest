# =================
# APP CONFIGURATION
# =================
from flask import Flask, render_template,send_file, make_response,request,jsonify
import os
import csv
from datetime import datetime, timedelta
import sqlite3
import zipfile
import bluey

app = Flask(__name__)
app.static_folder = 'static'


# =================
# APP FUNCTIONS
# =================

def getDataforDays(numdays):
    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Fetch all data from the table
    c.execute("SELECT * FROM data_table")
    rows = c.fetchall()

    recent_data = []
    now = datetime.now()    

    for row in rows:
        timestamp_str = row[0]  # Assuming the timestamp is in the first column
        timestamp = datetime.strptime(timestamp_str, "%Y/%m/%d %H:%M")

        if now - timestamp < timedelta(days=numdays):
            data_dict = {
                "Timestamp": timestamp_str,
                "Location": row[1],  # Assuming the location is in the second column
                "Temperature": row[2],  # Assuming the temperature is in the third column
                "Humidity": row[3],  # Assuming the humidity is in the fourth column
                "Filename": row[4]  # Assuming the filename is in the fifth column
            }
            recent_data.append(data_dict)

    recent_data.reverse()
    # Close the database connection
    conn.close()
    return recent_data

# =================
# APP ROUTES
# =================

# Route for camerapreview.html
@app.route('/')
def camera_preview():
    return render_template('camerapreview.html')

# Route for datapreview.html
@app.route('/datapreview/<timespan>')
def data_previewdays(timespan):
    
    if timespan == "1":
        data = getDataforDays(1)
        return render_template('datapreview.html',buttonval = "Last 24 Hours",pagedata = data)
    if timespan == "7":
        data = getDataforDays(7)
        return render_template('datapreview.html',buttonval = "Last 7 Days",pagedata = data)
    if timespan == "30":
        data = getDataforDays(30)
        return render_template('datapreview.html',buttonval = "Last 30 Days",pagedata = data)
    data = getDataforDays(30)
    return render_template('datapreview.html',buttonval = "Last 30 Days",pagedata = data)


# Route for datapreview.html
@app.route('/datapreview/')
def data_preview():
    data = getDataforDays(30)
    return render_template('datapreview.html',buttonval = "Last 30 Days",pagedata = data)

# Route for dataretrieval.html
@app.route('/dataretrieval')
def data_retrieval():
    return render_template('dataretrieval.html')


# Route for dataretrieval.html
@app.route('/settings')
def settings():
    with open('saved_devices.txt', 'r') as file:
    # Read all lines from the file into a list
        lines = [x.strip() for x in file.readlines()]
    lines = lines[1:]
    lines = [x.split(",")[1] for x in lines]
    print(lines)

    return render_template('settings.html',lines=lines)



@app.route('/image/<image_name>')
def serve_image(image_name):
    if image_name == "camera_preview_inside.png":
        # Fetch latest image here
        image_path = "../Previews/inside.png"
    elif image_name == "camera_preview_outside.png":
        # Fetch latest image here
        image_path = "../Previews/outside.jpg"
    else: 
        image_path = os.path.join('../System_Pics/', image_name+".jpg")
    return send_file(image_path, mimetype='image/jpg')


@app.route('/video/<video_name>')
def serve_video(video_name):

    video_path = os.path.join('../Videos/split/', video_name)
    response = make_response(send_file(video_path, mimetype='video/mp4'))
    response.headers['Content-Disposition'] = 'inline'
    return response

# =================
# APP API ROUTES 
# =================

@app.route('/api/gendata', methods=['POST'])
def gen_data():
    # Get the data from the request
    data = request.get_json()

    # Extract the values from the data
    begin_date = data.get('beginDate').replace("-","/")
    end_date = data.get('endDate').replace("-","/")
    pictures = data.get('pictures')
    videos = data.get('videos')
    temps = data.get('temps')
    humidity = data.get('humidity')
    output_format = data.get('outputFormat')
    
    # Query Database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data_table WHERE Timestamp BETWEEN ? AND ?", (f"{begin_date} 00:00", f"{end_date} 23:59"))
    rows = c.fetchall()

    # output filename
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = current_datetime+".csv"
    
    # add files
    files_to_add = []
    for item in rows:
        if videos:
            video_path = os.path.join('../Videos/split/', item[4]+".mp4")
            files_to_add.append(video_path)
        if pictures:
            image_path = os.path.join('../System_Pics/', item[4]+".jpg")
            files_to_add.append(image_path)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        output = ["Date", "Location"]
        if temps:
            output.append("Temperature")
        if humidity:
            output.append("Humidity")
        if pictures or videos:
            output.append("Filename")
        writer.writerow(output)

        for row in rows:
            output = [row[0], row[1]]
            if temps:
                output.append(row[2])
            if humidity:
                output.append(row[3])
            if pictures or videos:
                output.append(row[4])
            writer.writerow(output)

    files_to_add.append(filename)

    zipfilename = os.path.join("static/outputs/",current_datetime + ".zip")

    with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as zipMe:
        for file in files_to_add:
            with open(file, 'rb') as f_in:
                zip_info = zipfile.ZipInfo(os.path.basename(file))
                zipMe.writestr(zip_info, f_in.read())
    # Return a response to indicate success
    print("Here")
    return jsonify({'status': 'success','zipfile':zipfilename})

@app.route('/api/addnearbydevices', methods=['POST'])
def add_nearby_devices():
    # Handle the request to add nearby devices
    print("Showing nearby devices")
    nearby_devices = bluey.get_nearby_devices()
    print(nearby_devices)
    print("Adding nearby devices")
    bluey.write_data_to_file(nearby_devices)
    return jsonify({'success': True})

@app.route('/api/setdatetime', methods=['POST'])
def set_datetime():
    data = request.get_json()
    datetime_str = data.get('dateTime')
    if datetime_str:
        # Convert the ISO string to a datetime object
        print(datetime_str.split(",")[0])
        current_datetime = datetime.fromisoformat(datetime_str)
        print(current_datetime)
        return jsonify({'success': True, 'dateTime': datetime_str})
    else:
        return jsonify({'success': False, 'error': 'Missing dateTime parameter'})

@app.route('/api/cleardata', methods=['POST'])
def clear_data():
    # Handle the request to clear data
    # ...
    print("Clearing data")
    return jsonify({'success': True})

@app.route('/api/level', methods=['POST'])
def set_level():
    data = request.get_json()
    level = data.get('level')
    # Handle the request to set the sensitivity level
    # ...
    return jsonify({'success': True, 'level': level})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)
    #,debug=True