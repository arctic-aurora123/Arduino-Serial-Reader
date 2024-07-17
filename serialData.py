import serial
import pandas as pd
import keyboard  # Import keyboard module for detecting keypress events
import time  # Import time module for delays
import os

file_path = os.path.abspath(__file__)
# Function to read serial data and save to xlsx using Pandas
def serial_and_save(serial_port, baudrate, data_names, xlsx_filename):
    # Initialize serial connection
    ser = serial.Serial(serial_port, baudrate)
    print(f"Reading serial data from {serial_port} at {baudrate} baudrate...")

    # Create an empty DataFrame with columns as data_names
    df = pd.DataFrame(columns=data_names)

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                data = line.split(',')
                if len(data) == len(data_names):
                    # Append data to DataFrame
                    df = pd.concat([df, pd.DataFrame([data], columns=data_names)], ignore_index=True)
                    print(f"Data received: {data}")
            
            # Check for Esc key press to break out of the loop
            if keyboard.is_pressed('esc'):
                print("Esc key pressed. Stopping serial reading.")
                break
            
            # Optional: Add a delay to control the rate of reading
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Stopping serial reading.")

    finally:
        # Close serial connection
        ser.close()
        print("Serial connection closed.")

        # Save DataFrame to xlsx
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xlsx_path = os.path.join(script_dir, xlsx_filename)
        df.to_excel(xlsx_path, index=False)
        print(f"Data saved to {xlsx_path}")
        print(df)

if __name__ == "__main__":
    # Input serial port and baudrate from user
    serial_port = input("Enter serial port (e.g., COM3 or /dev/ttyUSB0): ")
    baudrate = int(input("Enter baudrate (e.g., 9600): "))

    # Input data names from user
    data_names = input("Enter names of each kind of data separated by commas (e.g., Temperature,Humidity): ").strip().split(',')

    # Define xlsx filename
    xlsx_filename = 'serial_data.xlsx'

    # Read serial data and save to xlsx using Pandas
    serial_and_save(serial_port, baudrate, data_names, xlsx_filename)
