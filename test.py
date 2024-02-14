import cv2
import sqlite3
import datetime
from pyzbar.pyzbar import decode

# Function to write decoded text to a text file
def write_to_file(text,converted):
    with open("decoded_text.txt", "a") as file:
        file.write(text +" "+converted+'\n')
    f=open('decoded_text.txt','r')
    l2=f.readlines()
    f2=open('new.txt','w')
    if len(l2)==1 or len(l2)==2:
        if len(l2)==1:
            f2.write(l2=[0])

        else:
            f2.write(l2[1])
    


# Open the camera
cap = cv2.VideoCapture(0)

while True:

    # Read a frame from the camera
    ret, frame = cap.read()

    # Decode QR codes from the frame
    decoded_objects = decode(frame)

    # If any QR code is detected, extract and write the decoded text to the text file
    for obj in decoded_objects:
        text = obj.data.decode('utf-8')
        print("Decoded text:", text)
        current_time=datetime.datetime.now()
        print(current_time)
        hours=current_time.hour
        minute=current_time.minute
        converted=hours*60+minute
        write_to_file(text,str(converted))

    # Display the frame
    cv2.imshow('QR Code Scanner', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
