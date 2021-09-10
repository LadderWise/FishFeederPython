from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import Window_1
import Data_base_extractor
import sqlite3
import signal
import time
import sys
import threading


def fill_daily_schedule_listbox():
    daily_schedule_listbox.delete(0, END)
    conn = sqlite3.connect('Value_holder.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM daily_schedules")
    items = c.fetchall()
                
    for item in items:
        hour = str(item[0])
        minute = str(item[1])
        daily_schedule_listbox.insert (END, hour + " : " + minute)
    conn.commit()
    conn.close()

def open_motor_control():
    window.destroy()
    Window_1.motor_control()
def open_schedule():
    window.destroy()
    Window_1.schedule()
def open_manual_override():
    window.destroy()
    Window_1.manual_override()

window = Tk()
window.title("Automatic Fish Feeder UI")
window.geometry("800x450")
window.resizable(0, 0)

my_canvas = Canvas(window, width=800, height=450, bg="#262424")
my_canvas.pack(fill="both", expand=True)

#FIXED TEXTS
#ROW TITLES
my_canvas.create_text(410, 50, text="Aquaculture Programmable Feeder", font=("Helvetica", 25), fill="white")
my_canvas.create_text(175, 120, text="SCHEDULE DETAILS", font=("Helvetica", 14), fill="white")
my_canvas.create_text(425, 120, text="STATUS", font=("Helvetica", 14), fill="white")
my_canvas.create_text(575, 120, text="TIMER", font=("Helvetica", 14), fill="white")
my_canvas.create_text(725, 120, text="STORAGE", font=("Helvetica", 14), fill="white")

#SCHEDULE
my_canvas.create_text(73, 160, text="SCHEDULE NAME:", font=("Helvetica", 11), fill="white")
my_canvas.create_text(103, 180, text="SPECIES:", font=("Helvetica", 11), fill="white")
my_canvas.create_text(70, 200, text="EST. POPULATION:", font=("Helvetica", 11), fill="white")
my_canvas.create_text(93, 220, text="FEED NAME:", font=("Helvetica", 11), fill="white")
my_canvas.create_text(78, 245, text="DAILY FEED ALLOWANCE", font=("Helvetica", 8), fill="white")
my_canvas.create_text(270, 245, text="DAILY FEEDING SCHEDULE", font=("Helvetica", 8), fill="white")
my_canvas.create_text(78, 285, text="DFA UPDATE PERIOD", font=("Helvetica", 8), fill="white")
my_canvas.create_text(78, 325, text="FEED INCREMENT", font=("Helvetica", 8), fill="white")
#units
my_canvas.create_text(110, 265, text="kg.", font=("Helvetica", 11), fill="white")
my_canvas.create_text(115, 305, text="days", font=("Helvetica", 11), fill="white")
my_canvas.create_text(110, 345, text="kg.", font=("Helvetica", 11), fill="white")

#STATUS
my_canvas.create_text(425, 160, text="MOTOR A", font=("Helvetica", 8), fill="white")
my_canvas.create_text(425, 240, text="MOTOR B", font=("Helvetica", 8), fill="white")
my_canvas.create_text(425, 320, text="SPEED CONTROL METHOD", font=("Helvetica", 8), fill="white")

#TIMER
my_canvas.create_text(575, 160, text="FEEDING COUNTDOWN", font=("Helvetica", 8), fill="white")
my_canvas.create_text(575, 240, text="NEXT FEEDING IN...", font=("Helvetica", 8), fill="white")

#STORAGE
my_canvas.create_text(725, 160, text="EST. FEEDS STORAGE LEVEL", font=("Helvetica", 8), fill="white")





#VARIABLE TEXTS
#SCHEDULE
schedule_name = my_canvas.create_text(250, 160, text=Data_base_extractor.get_value_holder()[0], font=("Helvetica", 11), fill="cyan")
species = my_canvas.create_text(250, 180, text=Data_base_extractor.get_value_holder()[1], font=("Helvetica", 11), fill="cyan")
population = my_canvas.create_text(250, 200, text=Data_base_extractor.get_value_holder()[2], font=("Helvetica", 11), fill="cyan")
feed_name = my_canvas.create_text(250, 220, text=Data_base_extractor.get_value_holder()[3], font=("Helvetica", 11), fill="cyan")
dfa = my_canvas.create_text(70, 265, text=Data_base_extractor.get_value_holder()[4], font=("Helvetica", 11), fill="green")
dfa_schedule = my_canvas.create_text(70, 305, text=Data_base_extractor.get_value_holder()[5], font=("Helvetica", 11), fill="green")
dfa_increment = my_canvas.create_text(70, 345, text=Data_base_extractor.get_value_holder()[6], font=("Helvetica", 11), fill="green")

#STATUS
motorA_status = my_canvas.create_text(425, 190, text="IDLE", font=("Helvetica", 16), fill="yellow")
motorB_status = my_canvas.create_text(425, 270, text="IDLE", font=("Helvetica", 16), fill="yellow")
speed_control_method = my_canvas.create_text(425, 340, text=Data_base_extractor.get_value_holder()[7], font=("Helvetica", 11), fill="cyan")

#TIMER
feeding_countdown = my_canvas.create_text(575, 190, text="---", font=("Helvetica", 16), fill="green")
next_feeding_countdown = my_canvas.create_text(575, 270, text="---", font=("Helvetica", 16), fill="green")





#FIXED SHAPES
my_canvas.create_rectangle(675, 180, 775, 300, fill="#444343")
#VARIABLE SHAPES
fishtank_bar = my_canvas.create_rectangle(680, 183, 770, 295, fill="orange", width=0)

#FIXED LINES
#horizontal
my_canvas.create_line(0, 100, 800, 100, fill="gray")
my_canvas.create_line(0, 140, 800, 140, fill="gray")
my_canvas.create_line(0, 365, 800, 365, fill="gray")

#vertical
my_canvas.create_line(350, 100, 350, 365, fill="gray")
my_canvas.create_line(500, 100, 500, 365, fill="gray")
my_canvas.create_line(650, 100, 650, 365, fill="gray")


#LISTBOX
daily_schedule_listbox = Listbox(window, font="Helvetica 8 bold", fg="gray", bg="white", height = 6, width = 25)
daily_schedule_window = my_canvas.create_window(190, 260, anchor="nw", window=daily_schedule_listbox)

#buttons
motor_control_button = Button(window, text = "MOTOR CONTROL", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 10, pady = 12, command=open_motor_control)
schedule_button = Button(window, text = "SCHEDULE", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 27, pady = 12, command=open_schedule)
manual_override_button = Button(window, text = "MANUAL OVER RIDE", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 7, pady = 12, command=open_manual_override)
calibration_button = Button(window, text = "CALIBRATION", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 27, pady = 12, command=lambda:Window_1.calibration())
information_button = Button(window, text = "INFORMATION", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 27, pady = 12, command=lambda:Window_1.information())
options_button = Button(window, text = "OPTIONS", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 30, pady = 12, command=lambda:Window_1.options())
storage_reset_button = Button(window, text = "FILL", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 35, pady = 0)




motor_control_window = my_canvas.create_window(5, 395, anchor="nw", window=motor_control_button)
schedule_window = my_canvas.create_window(135, 395, anchor="nw", window=schedule_button)
manual_override_window = my_canvas.create_window(260, 395, anchor="nw", window=manual_override_button)
calibration_window = my_canvas.create_window(394, 395, anchor="nw", window=calibration_button)
information_window = my_canvas.create_window(536, 395, anchor="nw", window=information_button)
options_window = my_canvas.create_window(679, 395, anchor="nw", window=options_button)
storage_reset_window = my_canvas.create_window(675, 310, anchor="nw", window=storage_reset_button)

fill_daily_schedule_listbox()

window.mainloop()












#***CODE ENDS HERE***
#C!O@D#E$D%B^Y&ARA639616183465
