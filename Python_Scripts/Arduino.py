import serial
import time
import numpy as np
import threading
import pyttsx3
import os
from PIL import Image, ImageTk
from joblib import load

photo_images = []
stop_event = threading.Event()
start_speaking = False
speaking_text = ""


def init_tts_engine():
    return pyttsx3.init()


def speak_in_thread():
    global speaking_text
    enginet = init_tts_engine()
    if enginet is not None:
        enginet.say(speaking_text)
        enginet.runAndWait()
    else:
        print("Text-to-speech engine not initialized.")


def say_the_letter():
    if start_speaking:
        try:
            t_speak = threading.Thread(target=speak_in_thread)
            t_speak.daemon = True
            t_speak.start()
        except:
            print("Could not start speaking thread!")
    else:
        pass


def arduino_glove(my_canvas11, my_canvas22, labelText1, oval11, oval22, oval33, image_item1):
    stop_event.clear()
    arduino_port = 'COM4'
    global photo_images
    global start_speaking
    global speaking_text

    gesture_labels = [
        "Not wearing glove",
        "Wearing glove",
        "letter A",
        "letter C",
        "Number 9",
        "letter I",
        "letter M",
        "Number 10",
        "letter X",
        "letter Y"
    ]
    folder_path = "Images"
    image_list = [
        Image.open(os.path.join(folder_path, "not_wearing.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "wearing.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "letter_A.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "letter_C.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "Number_9.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "letter_I.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "letter_M.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "Number_10.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "letter_X.png")).resize((350, 252), resample=Image.LANCZOS),
        Image.open(os.path.join(folder_path, "letter_Y.png")).resize((350, 252), resample=Image.LANCZOS),
    ]

    last_predicted_label = None  # Initializing last predicted label
    # Loading the saved classifier
    classifier = load('knn_classifier_model.joblib')

    # Open serial port with baud 9600 and timeout of 1 second
    ser = serial.Serial(arduino_port, 9600, timeout=1)

    # Wait a good while (3s) for the Arduino and the computer to connect
    time.sleep(3)
    print(f"Connected to arduino port: {arduino_port}")

    ser.write(b'1')

    try:
        # Clearing any data that maybe accidentally in the serial port
        ser.flush()

        while not stop_event.is_set():
            # Read line from serial
            line = ser.readline()
            # if got sensor value, classifying it
            if len(line) > 0:
                # Getting the raw values
                raw_values = line.decode().strip().split(',')

                # Convert string values to integers
                values = list(map(int, raw_values))
                # Classifying the value
                values2 = np.array(values).reshape(-1, 6)
                label = classifier.predict(values2)
                label_index = int(label[0])
                # print(f"{values2}  Predicted label:{label_index}  Gesture:{gesture_labels[label_index]}")

                # Updating the canvas items only when the prediction changes
                if label_index != last_predicted_label:
                    last_predicted_label = label_index

                    while len(photo_images) <= label_index:
                        photo_images.append(None)

                    # printing the label
                    if 0 <= label_index < len(gesture_labels):
                        my_canvas11.itemconfigure(labelText1, text=gesture_labels[label_index])
                        if photo_images[label_index] is None:
                            photo_images[label_index] = ImageTk.PhotoImage(image_list[label_index])
                        my_canvas11.itemconfigure(image_item1, image=photo_images[label_index])
                        if gesture_labels[label_index] in ["Wearing glove", "letter A", "letter C", "Number 9",
                                                           "letter I",
                                                           "letter M", "Number 10", "letter X", "letter Y"]:
                            my_canvas22.itemconfig(oval11, fill="green")
                            my_canvas22.itemconfig(oval22, fill="red")
                        elif gesture_labels[label_index] in ["Not wearing glove"]:
                            my_canvas22.itemconfig(oval11, fill="red")
                            my_canvas22.itemconfig(oval22, fill="green")

                        if start_speaking:
                            speaking_text = gesture_labels[label_index]
                            my_canvas22.itemconfig(oval33, fill="green")
                            # speak_text(gesture_labels[label_index], my_canvas22, oval33)
                    else:
                        print("Cannot detect unfortunately!")

    except Exception as e:
        print(e)
        ser.close()
    finally:
        print("Execution stopped!")


def execute_arduino_glove(my_canvas11, my_canvas22, labelText1, oval11, oval22, oval33, image_item1):
    try:
        t_arduino = threading.Thread(target=arduino_glove,
                                     args=(my_canvas11, my_canvas22, labelText1, oval11, oval22, oval33, image_item1))
        t_arduino.daemon = True
        t_arduino.start()
    except:
        print("Could not start predicting!")
        return


def stop_arduino_thread(my_canvas11, my_canvas22, labelText1, oval11, oval22, oval33, image_item1):
    stop_event.set()
    blank_image = Image.new('RGBA', (350, 252), (0, 0, 0, 0))
    blank_photo = ImageTk.PhotoImage(blank_image)
    my_canvas11.itemconfigure(labelText1, text="")
    my_canvas22.itemconfig(oval11, fill="red")
    my_canvas22.itemconfig(oval22, fill="red")
    my_canvas22.itemconfig(oval33, fill="red")
    my_canvas11.itemconfigure(image_item1, image=blank_photo)


def execute_speaking():
    global start_speaking
    start_speaking = True


def turn_off_speaking(my_canvas22, oval33):
    global start_speaking
    start_speaking = False
    my_canvas22.itemconfig(oval33, fill="red")


def say_the_letter_periodically(root):
    say_the_letter()  # Call the function
    root.after(1800, lambda: say_the_letter_periodically(root))
