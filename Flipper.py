import usb.core
import usb.util
import bluetooth
import serial
import os
import subprocess
from rich.console import Console
from rich.table import Table
import time


# USB Device Management
def list_usb_devices():
    devices = usb.core.find(find_all=True)
    for device in devices:
        print(f"Device: {device}")
        print(f"  ID Vendor: {device.idVendor}")
        print(f"  ID Product: {device.idProduct}")
        print(f"  Manufacturer: {usb.util.get_string(device, device.iManufacturer)}")
        print(f"  Product: {usb.util.get_string(device, device.iProduct)}")
        print('-' * 40)


# RFID Scanning (RFID Reader connected via serial)
def read_rfid():
    try:
        with serial.Serial('/dev/ttyUSB0', 9600) as ser:
            print("RFID Reader is connected!")
            while True:
                data = ser.readline()
                print(f"RFID Data: {data.decode('utf-8').strip()}")
    except Exception as e:
        print(f"Error reading RFID: {e}")


# Bluetooth Scanning
def scan_bluetooth_devices():
    print("Scanning for Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True, lookup_uuids=True)
    for addr, name in nearby_devices:
        print(f"Found device: {name} - {addr}")


# IR Signal Capture
def capture_ir_signal():
    try:
        print("Capturing IR signal...")
        os.system("irrecord -d /dev/lirc0 ~/my_ir_signal.conf")
        print("IR Signal Captured Successfully.")
    except Exception as e:
        print(f"Error capturing IR signal: {e}")


# IR Transmitting (Using LIRC)
def send_ir_signal():
    try:
        os.system("irsend SEND_ONCE samsung_volume_up")
        print("IR signal sent!")
    except Exception as e:
        print(f"Error sending IR signal: {e}")


# Menopoleter (Signal Manipulation)
def manipulete_signal():
    print("Manipulating captured signal...")
    try:
        # Example: Signal manipulation by modifying the IR signal's frequency or data
        subprocess.call(['irsend', 'SEND_ONCE', 'samsung', 'power_on'])
        print("Signal Manipulated and Transmitted.")
    except Exception as e:
        print(f"Error manipulating signal: {e}")


# GPIO Control (using Termux API)
def control_gpio():
    try:
        os.system('termux-battery-status')
        print("GPIO control is ready!")
    except Exception as e:
        print(f"Error controlling GPIO: {e}")


# Create a pretty table for the menu using Rich
def create_table():
    console = Console()
    table = Table(title="Flipper Zero Tools")
    
    table.add_column("Feature", style="bold cyan")
    table.add_column("Status", style="bold green")
    
    table.add_row("USB Device Management", "Active")
    table.add_row("RFID Scanning", "Active")
    table.add_row("Bluetooth Scanning", "Inactive")
    table.add_row("IR Transmit", "Inactive")
    table.add_row("IR Capture", "Inactive")
    table.add_row("Menopoleter (Signal Manipulation)", "Inactive")
    table.add_row("GPIO Control", "Active")
    
    console.print(table)


# Main Menu to interact with the tool
def main_menu():
    create_table()
    print("\nFlipper Zero Tools Menu")
    print("1. List USB Devices")
    print("2. Scan RFID")
    print("3. Scan Bluetooth")
    print("4. Send IR Signal")
    print("5. Capture IR Signal")
    print("6. Manipulate Signal (Menopoleter)")
    print("7. Control GPIO")
    print("0. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        list_usb_devices()
    elif choice == "2":
        read_rfid()
    elif choice == "3":
        scan_bluetooth_devices()
    elif choice == "4":
        send_ir_signal()
    elif choice == "5":
        capture_ir_signal()
    elif choice == "6":
        manipulete_signal()
    elif choice == "7":
        control_gpio()
    elif choice == "0":
        exit()
    else:
        print("Invalid choice. Try again.")


if __name__ == "__main__":
    while True:
        main_menu()
