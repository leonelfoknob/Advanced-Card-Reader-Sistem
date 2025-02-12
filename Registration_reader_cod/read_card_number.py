import serial.tools.list_ports
import time

def find_arduino():
    """Automatically find the Arduino's serial port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description:
            return port.device  # Return the port name (e.g., COM3 or /dev/ttyUSB0)
    return None

def read_card_id(serial_port):
    """Read card ID from the Arduino."""
    try:
        with serial.Serial(serial_port, 9600, timeout=1) as ser:
            print("Listening for card IDs...")
            while True:
                if ser.in_waiting > 0:
                    card_id = ser.readline().decode("utf-8").strip()
                    print(f"Card ID: {card_id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    port = find_arduino()
    if port:
        print(f"Arduino found on port: {port}")
        read_card_id(port)
    else:
        print("Arduino not found. Please check the connection.")
