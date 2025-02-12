#bu kod raspberry pi 5te bu şekilde otomatic başlatıldım
#crontab -e
#@reboot sleep 10 && export DISPLAY=:0 && export XAUTHORITY=/home/leonel/.Xauthority && sudo /usr/bin/python3 /home/leonel/card_main/scripts/main_1.py >> /home/leonel/script_log.txt 2>&1
# +SI:localuser:root

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import pymysql
import tkinter as tk
from tkinter import messagebox
import threading

# Database connection
Host = "localhost"
User = "******"
Password = "*******"
database = "********"

conn = pymysql.connect(host=Host, user=User, password=Password, db=database)
cur = conn.cursor()

red_led = 24
blue_led = 23
relay = 22
buzzer = 25

flag_control = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(blue_led, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

# GUI setup
root = tk.Tk()
root.title("Card Reader")

# Hide the title bar (make window borderless)
root.overrideredirect(True)

# Set the size of the window
root.geometry("800x500")  # Width x Height

# Labels for displaying card info
#name_label = tk.Label(root, text="Name: ", font=("Helvetica", 16), anchor="center")
#credit_label = tk.Label(root, text="Credit: ", font=("Helvetica", 16), anchor="center")

name_label = tk.Label(root, text="", font=("Helvetica", 30), anchor="center")
credit_label = tk.Label(root, text="Credit: ", font=("Helvetica", 30), anchor="center")

# Function to update the GUI based on card detection
def update_gui(name, credit):
    if name and credit is not None:
        name_label.config(text=f"{name}")
        credit_label.config(text=f"Credit: {credit}")
        name_label.pack(expand=True)
        credit_label.pack(expand=True)
        root.deiconify()  # Show the window

        # Set background color based on credit status
        if credit > 0:
            root.config(bg="green")  # Sufficient credit
        elif credit == 0:
            root.config(bg="red")  # No more credit
        else:
            root.config(bg="red")  # Not registered

        root.after(2000, root.withdraw)  # Hide after 3 seconds
    else:
        name_label.pack_forget()
        credit_label.pack_forget()
        root.withdraw()  # Hide the window

# Functions to play different buzzer sounds
def kart_okumus_sesi():
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.2)

def hatasiz_kart_sesi():
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.2)

def hatali_kart_sesi():
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.1)

# Function to convert UID to string
def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = format(i, '02X') + mystring
    return mystring

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    root.quit()  # Exit Tkinter loop when script ends

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# Function to handle card detection in a separate thread
def read_card():
    continue_reading = True
    while continue_reading:
        GPIO.output(red_led, GPIO.HIGH)
        GPIO.output(blue_led, GPIO.LOW)
        GPIO.output(relay, GPIO.HIGH)
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        
        if status == MIFAREReader.MI_OK:
            print("Card detected")
            (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
            
            if status == MIFAREReader.MI_OK:
                UID = uidToString(uid)
                query1 = f"SELECT * FROM kayit WHERE (UID = %s)"
                result = cur.execute(query1, (UID,))
                data = cur.fetchone()
                
                if result >= 1:
                    print(data)
                    credit = int(data[11]) if data[11] is not None else 0
                    name = data[1]
                    
                    if credit <= 0:
                        print("Insufficient credit. Please reload.")
                        GPIO.output(red_led, GPIO.HIGH)
                        hatali_kart_sesi()
                        update_gui(name, 0)
                    else:
                        credit -= 1
                        print(f"Welcome! Remaining credit: {credit}")
                        hatasiz_kart_sesi()
                        GPIO.output(blue_led, GPIO.HIGH)
                        GPIO.output(red_led, GPIO.LOW)
                        update_gui(name, credit)
                        
                    # Update the database with new credit
                    cur.execute("UPDATE kayit SET credit = %s WHERE UID = %s", (credit, UID))
                    query1 = f"INSERT INTO yoklama (name, surname, branch, national_id, credit) VALUES ('{name}', '{data[2]}', '{data[4]}', '{data[8]}', {credit})"
                    cur.execute(query1)
                    conn.commit()
                    
                    time.sleep(2)
                else:
                    hatali_kart_sesi()
                    GPIO.output(red_led, GPIO.HIGH)
                    GPIO.output(blue_led, GPIO.LOW)
                    print("Card not registered.")
                    update_gui("Not Registered", 0)

# Start the card reader in a separate thread
card_thread = threading.Thread(target=read_card)
card_thread.daemon = True  # Ensure it exits when the main program exits
card_thread.start()

# Start Tkinter event loop
root.withdraw()  # Start by hiding the window
root.mainloop()

