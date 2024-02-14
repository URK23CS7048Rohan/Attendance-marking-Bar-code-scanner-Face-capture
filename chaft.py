import cv2
import sqlite3
from pyzbar.pyzbar import decode
from datetime import datetime
import time

# Connect to SQLite database
conn = sqlite3.connect('attendance_marking.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, event_type TEXT, timestamp DATETIME)''')


# Function to write time duration to a text file
def write_duration_to_file(login_time, logout_time, duration):
    with open("time_durations.txt", "a") as file:
        file.write(f"Login Time: {login_time}, Logout Time: {logout_time}, Duration: {duration}\n")


# Function to write event to database
def write_to_database(event_type, data, timestamp):
    c.execute("INSERT INTO attendance (data, event_type, timestamp) VALUES (?, ?, ?)", (data, event_type, timestamp))
    conn.commit()


# Function to handle login event
def handle_login(text, timestamp):
    print("Login event detected:", text)
    write_to_database("Login", text, timestamp)


# Function to handle logout event
def handle_logout(text, timestamp):
    print("Logout event detected:", text)
    write_to_database("Logout", text, timestamp)


# Open the camera
cap = cv2.VideoCapture(0)

last_scan_data = None
last_scan_time = None
login_time = None

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Decode QR codes from the frame
    decoded_objects = decode(frame)

    # If any QR code is detected, extract and handle the event
    for obj in decoded_objects:
        text = obj.data.decode('utf-8')
        print("Decoded text:", text)
        time.sleep(2)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # If this is the first scan or a logout event, handle it as login
        if last_scan_data is None or "logout" in text.lower():
            login_time = current_time
            handle_login(text, current_time)
        else:
            # Handle logout event
            handle_logout(text, current_time)

            # Calculate time duration and write to file
            duration = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S")
            print("Time duration:", duration)
            write_duration_to_file(login_time, current_time, duration)

        last_scan_data = text
        last_scan_time = current_time

    # Display the frame
    cv2.imshow('QR and Barcode Scanner', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1)== ord('e'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

# Close SQLite connection
conn.close()
