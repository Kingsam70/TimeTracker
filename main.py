from tkinter import *
import time
import threading
import playsound
from tkinter import messagebox

# You can change the below variables as per you like
BG_COLOR = "darkslategray"
BUTTON_COLOR = "white"
FG_TIMER_TEXT = "white"
FG_BUTTON_TEXT = "black"
LABEL_TEXT_COLOR = "white"


timer = None
timer_duration = 0
user_defined_time = 0


def start_timer():
    """starts the clock as per timer and when the timer is over plays a sound."""
    global timer, timer_duration

    hour = int(timer_duration / 3600)
    minute = int((timer_duration % 3600) / 60)
    second = int((timer_duration % 3600) % 60)

    # Below to give additional 0 if hour/minute/second are less than 10
    if hour < 10:
        hour = f"0{hour}"
    if minute < 10:
        minute = f"0{minute}"
    if second < 10:
        second = f"0{second}"

    canvas.itemconfig(canvas_text, text=f"{hour}:{minute}:{second}")

    if timer_duration == 0:  # Quitting function if timer is over
        threading.Thread(target=play_sound).start()
        return

    timer_duration -= 1
    timer = window.after(1000, start_timer)


def play_sound():
    time.sleep(1)  # Delay the sound by 1 second in as to play below sound exactly at 0 seconds

    # Do change the below path for your sound file It'll only work for me.
    try:
        playsound.playsound("./clock_alarm.mp3")
    except:
        print("If you do not want the system to play any sound, you can leave the sound path empty or provide a path to a sound file.")


def stop_timer():
    global timer

    if timer is not None:  # This line of code means the stop button will only work when the timer is running
        window.after_cancel(timer)


def resume_timer():
    global timer
    start_timer()


def reset_timer():
    global timer_duration
    if timer is not None:
        window.after_cancel(timer)
    canvas.itemconfig(canvas_text, text="00:00:00")
    timer_duration = user_defined_time


def add_time():
    """adds the time which user provided in the entry in time_duration, Basically this time is the timer time"""
    global timer_duration, user_defined_time

    try:
        user_defined_time = int(time_entry.get())
        timer_duration = user_defined_time
    except ValueError:
        messagebox.showwarning(message="Does not support floating point values.")
        print("Only woks with seconds not with milliseconds, So please dont give float value.")


window = Tk()
window.config(padx=20, pady=20, bg=BG_COLOR)
window.title("Timer")
icon_image = PhotoImage(file="./stopwatch_png.png")
window.iconphoto(False, icon_image)

# Below for creating canvas onto which we can place a number of things.
canvas = Canvas(height=224, width=200, bg=BG_COLOR, highlightthickness=0)
canvas.grid(column=1, row=2)

# Below code for the creation of the time text onto the canvas
canvas_text = canvas.create_text(102, 120, text="00:00:00", fill=FG_TIMER_TEXT, font='Helvetica 30 bold')

# Creating an entry for amount of time
time_entry = Entry(width=10)
time_entry.focus()
time_entry.insert(0, str(1800))  # Defaults to 30-min timer (time should be in seconds)
time_entry.grid(column=1, row=1)

# Creating Buttons
start_button = Button(text="Start", width=7, bg=BUTTON_COLOR, fg=FG_BUTTON_TEXT, command=start_timer)
start_button.grid(column=1, row=3, pady=20)

stop_button = Button(text="Stop", width=7, bg=BUTTON_COLOR, fg=FG_BUTTON_TEXT, command=stop_timer)
stop_button.grid(column=0, row=3, pady=20)

resume_button = Button(text="Resume", width=7, bg=BUTTON_COLOR, fg=FG_BUTTON_TEXT, command=resume_timer)
resume_button.grid(column=2, row=3, pady=20)

reset_image = PhotoImage(file="./image_reset.png")
reset_button = Button(image=reset_image, command=reset_timer)
reset_button.grid(column=0, row=0)

add_entry_button = Button(text="Add time", bg=BUTTON_COLOR, fg=FG_BUTTON_TEXT, command=add_time)
add_entry_button.grid(column=2, row=0)

# Creating timer label
timer_label = Label(text="Enter Time(sec) below\nThen click on Add Button.", font="Arial 10 bold", bg=BG_COLOR, fg=LABEL_TEXT_COLOR)
timer_label.grid(column=1, row=0)


window.mainloop()


