import serial
import time
import os

arduino_port = 'COM4'

data_directory = "Testing_set/Shubhajit1"  # change to testing or training set for collecting respective datas

# Creating the data directory if it doesn't exist
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Predefined list of file names
fileName = [os.path.join(data_directory, "Not_wearing_glove.csv"),
            os.path.join(data_directory, "wore_glove.csv"),
            os.path.join(data_directory, "letter_A.csv"),
            os.path.join(data_directory, "letter_C.csv"),
            os.path.join(data_directory, "Number_9.csv"),
            os.path.join(data_directory, "letter_I.csv"),
            os.path.join(data_directory, "letter_M.csv"),
            os.path.join(data_directory, "Number_10.csv"),
            os.path.join(data_directory, "letter_X.csv"),
            os.path.join(data_directory, "letter_Y.csv")]
samples = 3000  # number of samples that needs to be collected

# Displaying available file names to the user
print("Available file names:")
for i, file_path in enumerate(fileName, 1):
    file_name = os.path.basename(file_path)  # Extracting the file name from the path
    print(f"{i}. {file_name}")

# User input for selecting a file
selected_index = int(input("Enter the number corresponding to the desired file: "))
selected_file = fileName[selected_index - 1]

# Open serial port with baud 9600 and timeout of 1 second
ser = serial.Serial(arduino_port, 9600, timeout=1)
print(f"Connected to arduino port: {arduino_port}")
file = open(selected_file, "w")

# Adding column headers to the file
headers = "thumb_sensor,index_finger_sensor,middle_finger_sensor,ring_finger_sensor,little_finger_sensor,palm_sensor\n"
file.write(headers)

print(f"Created the file {selected_file}")

# Wait a good while (3s) for the Arduino and the computer to connect
time.sleep(3)

ser.write(b'1')

print(ser.writable())

i = 0
while i < samples:
    getValue = str(ser.readline())
    line = getValue[2:][:-5]
    print(line)
    file = open(selected_file, "a")
    file.write(line + "\n")
    i = i + 1

ser.write(b'0')
print("Data has been collected!")
ser.close()
file.close()

# Reference: https://www.youtube.com/watch?v=vayAp84vea8
