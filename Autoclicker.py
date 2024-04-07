import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time

# Function to automate clicks
def automate_clicks(duration, interval, position):
    end_time = time.time() + duration * 60  # Convert minutes to seconds
    while time.time() < end_time and not stop_event.is_set():
        pyautogui.click(x=position[0], y=position[1])
        time.sleep(interval)

# Function to start the automation on a separate thread
def start_clicking():
    global stop_event
    stop_event.clear()
    duration = float(duration_entry.get())
    interval = float(interval_entry.get())
    position = (int(x_entry.get()), int(y_entry.get()))
    t = threading.Thread(target=automate_clicks, args=(duration, interval, position))
    t.start()

# Function to stop the automation
def stop_clicking():
    stop_event.set()

# Function to select a position on the screen
def select_position():
    info_label.config(text="Click anywhere on the screen to select the position.")
    root.update()
    position = pyautogui.position()
    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)
    x_entry.insert(0, str(position.x))
    y_entry.insert(0, str(position.y))
    info_label.config(text="Position selected. You can start the automation.")

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("400x200")
root.attributes("-alpha", 0.9)  # Semi-transparent window

stop_event = threading.Event()

# Duration
duration_label = ttk.Label(root, text="Duration (minutes):")
duration_label.pack()
duration_entry = ttk.Entry(root)
duration_entry.pack()

# Interval
interval_label = ttk.Label(root, text="Interval (seconds):")
interval_label.pack()
interval_entry = ttk.Entry(root)
interval_entry.pack()

# Position X
x_label = ttk.Label(root, text="X Coordinate:")
x_label.pack()
x_entry = ttk.Entry(root)
x_entry.pack()

# Position Y
y_label = ttk.Label(root, text="Y Coordinate:")
y_label.pack()
y_entry = ttk.Entry(root)
y_entry.pack()

# Select position button
select_position_button = ttk.Button(root, text="Select Position", command=select_position)
select_position_button.pack()

# Start button
start_button = ttk.Button(root, text="Start", command=start_clicking)
start_button.pack()

# Stop button
stop_button = ttk.Button(root, text="Stop", command=stop_clicking)
stop_button.pack()

# Info label
info_label = ttk.Label(root, text="Enter values and click start.")
info_label.pack()

root.mainloop()
