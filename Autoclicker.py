import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time
from plyer import notification

# Main function to automate clicks
def automate_clicks(duration, interval, position):
    end_time = time.time() + duration * 60  # Convert minutes to seconds
    while time.time() < end_time and not stop_event.is_set():
        pyautogui.click(x=position[0], y=position[1])
        time.sleep(interval * 60)  # Convert minutes to seconds

# Starts the clicking process in a separate thread
def start_clicking():
    if not all([duration_entry.get(), interval_entry.get(), x_entry.get(), y_entry.get()]):
        info_label.config(text="Please fill in all fields.")
        return
    try:
        user_interaction()
        duration = float(duration_entry.get())
        interval = float(interval_entry.get())
        position = (int(x_entry.get()), int(y_entry.get()))
        stop_event.clear()
        t = threading.Thread(target=automate_clicks, args=(duration, interval, position), daemon=True)
        t.start()
        info_label.config(text="Clicking started...")
    except ValueError:
        info_label.config(text="Please enter valid numbers.")
    

# Stops the clicking process
def stop_clicking():
    user_interaction()
    stop_event.set()
    info_label.config(text="Clicking stopped.")

# Resets all settings to their initial values
def reset_settings():
    user_interaction()
    stop_clicking()
    duration_entry.delete(0, tk.END)
    interval_entry.delete(0, tk.END)
    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)
    info_label.config(text="Settings reset. Enter new values.")

# Custom close function to properly terminate the application
def user_interaction():
    global last_interaction_time
    last_interaction_time = time.time()

def on_close():
    stop_clicking()
    root.destroy()

# Function to send a notification after 20 minutes of inactivity
def notify_user():
    notification.notify(
        title='Auto Clicker Notification',
        message='It has been 20 minutes since your last interaction with the auto-clicker.',
        app_name='Auto Clicker'
    )

# Function to check for user inactivity and trigger notification
def schedule_notification():
    if time.time() - last_interaction_time >= 1200:  # 20 minutes
        notify_user()
    root.after(1200 * 1000, schedule_notification)  # Reschedule check every 20 minutes

def select_position(event=None):
    info_label.config(text="Move the cursor to the desired position and press 'F'.")
    root.update_idletasks()
    root.wait_variable(position_selected)

# Function to log the last time the user interacted with the program
def user_interaction():
    global last_interaction_time
    last_interaction_time = time.time()

def on_key_press(event):
    if event.char == 'f':
        position_selected.set(1)
        x_entry.delete(0, tk.END)
        y_entry.delete(0, tk.END)
        position = pyautogui.position()
        x_entry.insert(0, str(position.x))
        y_entry.insert(0, str(position.y))
        info_label.config(text="Position selected.")


# Initialize main window
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("350x400")
root.configure(bg='#333')
root.protocol("WM_DELETE_WINDOW", on_close)

# Set up threading event and interaction timer
stop_event = threading.Event()
last_interaction_time = time.time()

# Schedule the first notification check
root.after(1200 * 1000, schedule_notification)

# Style configuration for dark theme
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', background='#444', foreground='white')
style.configure('TLabel', background='#333', foreground='white')
style.configure('TEntry', background='#444', foreground='black', insertbackground='black')

# Info label
info_label = ttk.Label(root, text="Enter values and click start.", style='TLabel')
info_label.pack()

# Duration
duration_label = ttk.Label(root, text="Duration (minutes):", style='TLabel')
duration_label.pack()
duration_entry = ttk.Entry(root, style='TEntry')
duration_entry.pack()

# Interval
interval_label = ttk.Label(root, text="Interval (minutes):", style='TLabel')
interval_label.pack()
interval_entry = ttk.Entry(root, style='TEntry')
interval_entry.pack()

# Position X
x_label = ttk.Label(root, text="X Coordinate:", style='TLabel')
x_label.pack()
x_entry = ttk.Entry(root, style='TEntry')
x_entry.pack()

# Position Y
y_label = ttk.Label(root, text="Y Coordinate:", style='TLabel')
y_label.pack()
y_entry = ttk.Entry(root, style='TEntry')
y_entry.pack()

# Start button
start_button = ttk.Button(root, text="Start", command=start_clicking)
start_button.pack()

# Stop button
stop_button = ttk.Button(root, text="Stop", command=stop_clicking)
stop_button.pack()

# Reset button
reset_button = ttk.Button(root, text="Reset", command=reset_settings)
reset_button.pack()

# Position selected flag
position_selected = tk.IntVar(value=0)
root.bind('<Key>', on_key_press)

# Position button
position_button = ttk.Button(root, text="Select Position", command=lambda: select_position())
position_button.pack()

# Start the main loop
root.mainloop()