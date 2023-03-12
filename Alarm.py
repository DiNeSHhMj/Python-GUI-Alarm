#######################
import datetime
import threading
import time
import tkinter as tk
import winsound
import pytz

#Define constants for the alarm clock
ALARM_SOUND = "Alarm.wav"
IST_TIME_ZONE = pytz.timezone('Asia/Kolkata')  # timezone for India
ALARM_TIME_FORMAT = "%H:%M:%S"  # format for the alarm time
DEFAULT_ALARM_TIME = "00:00:00"  # default alarm time
SNOOZE_TIME_INTERVAL = 5  # snooze time in seconds

class AlarmClock:
    def __init__(self, root):
    #initialize the tkinter window
        self.root = root
        self.root.title("Python Alarm Clock")
        self.root.geometry("300x200")
        self.root.resizable(0, 0)
        
    #Create the label to display the current time
        self.time_label = tk.Label(self.root, font=("Arial", 20))
        self.time_label.pack(pady=10)
        
    # Create the entry field for setting the alarm time
        self.set_alarm_entry = tk.Entry(self.root, font=("Arial", 16))
        self.set_alarm_entry.insert(0, DEFAULT_ALARM_TIME)
        self.set_alarm_entry.pack(pady=10)
            
    # Create the button to set the alarm
        self.set_alarm_button = tk.Button(self.root, text="Set Alarm", font=("Arial", 16), command=self.set_alarm)
        self.set_alarm_button.pack(pady=10)
        
    # Create the button to snooze the alarm
        self.snooze_button = tk.Button(self.root, text="Snooze", font=("Arial", 16), height=50, state=tk.DISABLED, command=self.snooze_alarm)
        self.snooze_button.pack(pady=1)

    # Create the button to snooze the alarm
        self.reset_button = tk.Button(self.root, text="Reset", font=("Arial", 16), state=tk.DISABLED, command=self.reset_alarm)
        self.reset_button.pack(pady=10)

    # Initialize alarm properties
        self.alarm_time = None
        self.alarm_set = False
        self.snooze_time = None

    # Start updating the current time
        self.update_time()

    def update_time(self):
    #Update the current time label every second.
        now = datetime.datetime.now(pytz.utc).astimezone(IST_TIME_ZONE)
        current_time = now.strftime(ALARM_TIME_FORMAT)
        self.time_label.config(text=current_time)
        self.check_alarm()
        self.root.after(1000, self.update_time)

    def set_alarm(self):
    #Set the alarm time and enable the snooze and reset buttons.
        self.alarm_time = datetime.datetime.strptime(self.set_alarm_entry.get(), ALARM_TIME_FORMAT).time()
        self.alarm_set = True
        self.snooze_time = None
        self.snooze_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def check_alarm(self):
    #Check if the alarm should ring and ring it if necessary.
        if self.alarm_set:
            now = datetime.datetime.now(pytz.utc).astimezone(IST_TIME_ZONE)
            current_time = now.time()
            if current_time >= self.alarm_time or (self.snooze_time is not None and current_time >= self.snooze_time):
                self.alarm_rings()

    def alarm_rings(self):
    # Disable the snooze button and reset button
        self.alarm_set = False
        self.snooze_time = None
        self.snooze_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        threading.Thread(target=winsound.PlaySound, args=(ALARM_SOUND, winsound.SND_FILENAME)).start()

    def snooze_alarm(self):
    #Calculates and sets the snooze time for the alarm to go off again.
        now = datetime.datetime.now(pytz.utc).astimezone(IST_TIME_ZONE)
        self.snooze_time = (now + datetime.timedelta(seconds=SNOOZE_TIME_INTERVAL)).time()

    def reset_alarm(self):
    #Resets the alarm state and disables snooze and reset buttons.
        self.alarm_set = False
        self.snooze_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        
#Starts the tkinter event loop.
root = tk.Tk()
app = AlarmClock(root)
root.mainloop()
