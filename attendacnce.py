import cv2
import sqlite3
from pyzbar.pyzbar import decode
from datetime import datetime
import time
l3=[]
# Connect to SQLite database
conn = sqlite3.connect('attendance_marking.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, timestamp DATETIME)''')


# Function to write time duration to a text file
def write_duration_to_file(data, duration):
    with open("time_durations.txt", "a") as file:
        file.write(f"Data: {data}, Duration: {duration}\n")
        

# Function to write decoded text to database
def write_to_database(text, timestamp):
    c.execute("INSERT INTO attendance (data, timestamp) VALUES (?, ?)", (text, timestamp))
    conn.commit()


# Open the camera
cap = cv2.VideoCapture(0)

last_scan_data = None
last_scan_time = None

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Decode QR codes from the frame
    decoded_objects = decode(frame)

    # If any QR code is detected, extract and write the decoded text to the database
    for obj in decoded_objects:
        text = obj.data.decode('utf-8')
        print("Decoded text:", text)
        time.sleep(2)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Write to database
        write_to_database(text, current_time)
        l3.append(current_time)
        if last_scan_data is not None:
            # Calculate time duration
            duration = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(last_scan_time, "%Y-%m-%d %H:%M:%S")
            
            print("Time duration:", duration)
            for i in l3:
                print(i)
            l3.clear()
            write_duration_to_file(last_scan_data, duration)

        last_scan_data = text
        last_scan_time = current_time

    # Display the frame
    cv2.imshow('QR and Barcode Scanner', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1)== ord('e'):
        break
    #time.sleep(0.5)
# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

# Close SQLite connection
conn.close()