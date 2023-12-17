import tkinter as tk
from Arduino import *
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Aalto University")
root.eval("tk::PlaceWindow . center")
# Disable window resizing for convenience
root.resizable(width=False, height=False)

frame1 = tk.Frame(root, width=1100, height=600)
frame1.grid(row=0, column=0)

label1 = tk.Label(root, text="Sign Language Detection", font=("Times", 18, "bold italic"))

# add the label to the top of the frame using grid method
# label1.grid(row=0, column=0, padx=10, pady=10, sticky="n")
label1.place(relx=0.5, rely=0, anchor="n")
my_canvas1 = tk.Canvas(root, width=700, height=490)
my_canvas2 = tk.Canvas(root, width=280, height=180)
my_canvas3 = tk.Canvas(root, width=280, height=300)
my_canvas1.place(x=300, y=100)
my_canvas2.place(x=10, y=30)
my_canvas3.place(x=800, y=10)

predictText = my_canvas1.create_text(100, 300, font=('freemono', 15, 'bold'), anchor='sw', fill="red",
                                     text="Prediction:")
labelText = my_canvas1.create_text(210, 300, font=('freemono', 15, 'bold'), anchor='sw', fill="green", text="")
wearingText = my_canvas2.create_text(70, 66, font=('freemono', 12, 'bold'), anchor='sw',
                                     text="Wearing the glove")

notWearingtext = my_canvas2.create_text(70, 95, font=('freemono', 12, 'bold'), anchor='sw',
                                        text="Not wearing the glove")

Speaking_text = my_canvas2.create_text(70, 125, font=('freemono', 12, 'bold'), anchor='sw',
                                       text="Speaking")

oval1 = my_canvas2.create_oval(50, 50, 60, 60, fill="red")
oval2 = my_canvas2.create_oval(50, 80, 60, 90, fill="red")
oval3 = my_canvas2.create_oval(50, 110, 60, 120, fill="red")
my_canvas1.create_rectangle(75, 3, 430, 260, outline='black', fill='#f2f2f2', width=2)

start_predicting_button = tk.Button(
    root,
    text="Start Predicting",
    borderwidth=2,
    relief="solid",
    command=lambda: execute_arduino_glove(my_canvas1, my_canvas2, labelText, oval1, oval2, oval3, image_item),
    width=15,
    bg="#dd3439",
    fg="white",  # Text color
    activebackground="#45a049",  # Background color when pressed
    activeforeground="white"  # Text color when pressed
)

start_predicting_window = my_canvas3.create_window(55, 130, anchor="nw", window=start_predicting_button)

stop_predicting_button = tk.Button(
    root,
    text="Stop Predicting",
    borderwidth=2,
    relief="solid",
    command=lambda: stop_arduino_thread(my_canvas1, my_canvas2, labelText, oval1, oval2, oval3, image_item),
    width=15,
    bg="#dd3439",
    fg="white",  # Text color
    activebackground="#45a049",  # Background color when pressed
    activeforeground="white"  # Text color when pressed
)

stop_predicting_window = my_canvas3.create_window(55, 165, anchor="nw", window=stop_predicting_button)

start_speaking_button = tk.Button(
    root,
    text="Start Speaking",
    borderwidth=2,
    relief="solid",
    command=lambda: execute_speaking(),
    width=15,
    bg="#db7a7d",
    fg="white",  # Text color
    activebackground="#45a049",  # Background color when pressed
    activeforeground="white"  # Text color when pressed
)

start_speaking_window = my_canvas3.create_window(55, 220, anchor="nw", window=start_speaking_button)

stop_speaking_button = tk.Button(
    root,
    text="Stop Speaking",
    borderwidth=2,
    relief="solid",
    command=lambda: turn_off_speaking(my_canvas2, oval3),
    width=15,
    bg="#db7a7d",
    fg="white",  # Text color
    activebackground="#45a049",  # Background color when pressed
    activeforeground="white"  # Text color when pressed
)

stop_speaking_window = my_canvas3.create_window(55, 255, anchor="nw", window=stop_speaking_button)


# Schedule the function to be called every 1.8 seconds
root.after(1800, lambda: say_the_letter_periodically(root))

# Open a default image
image = Image.open("init.png")
image = image.resize((350, 252), resample=Image.LANCZOS)  # Resize image
photo = ImageTk.PhotoImage(image)
image_item = my_canvas1.create_image(78, 5, anchor="nw", image=photo)

# run application
root.mainloop()
