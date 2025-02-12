import serial.tools.list_ports
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time


def find_arduino():
    """Automatically find the Arduino's serial port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description:
            return port.device
    return None


def read_card_id(serial_port, gui_app):
    """Continuously read the card ID from the Arduino and update the GUI."""
    try:
        with serial.Serial(serial_port, 9600, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    card_id = ser.readline().decode("utf-8").strip()
                    gui_app.update_card_id(card_id)
    except Exception as e:
        gui_app.show_error(f"Error: {e}")


class CardReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Reader GUI")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        # UI Elements
        self.label = tk.Label(root, text="Card UID", font=("Arial", 16))
        self.label.pack(pady=10)

        self.card_id_var = tk.StringVar()
        self.card_id_entry = tk.Entry(
            root, textvariable=self.card_id_var, font=("Arial", 14), width=25
        )
        self.card_id_entry.pack(pady=10)

        self.copy_button = tk.Button(
            root,
            text="Copy UID",
            font=("Arial", 12),
            command=self.copy_to_clipboard,
            state=tk.DISABLED,
        )
        self.copy_button.pack(pady=10)

        # Auto-detect Arduino
        self.serial_port = find_arduino()
        if self.serial_port:
            self.start_reading()
        else:
            self.show_error("Arduino not found. Please check the connection.")

    def start_reading(self):
        """Start a separate thread to read card IDs."""
        Thread(target=read_card_id, args=(self.serial_port, self), daemon=True).start()

    def update_card_id(self, card_id):
        """Update the card ID in the GUI."""
        self.card_id_var.set(card_id)
        self.copy_button.config(state=tk.NORMAL)

    def copy_to_clipboard(self):
        """Copy the card ID to the clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.card_id_var.get())
        self.root.update()  # Update the clipboard
        messagebox.showinfo("Copied", "Card UID copied to clipboard!")

    def show_error(self, message):
        """Show an error message."""
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = CardReaderApp(root)
    root.mainloop()