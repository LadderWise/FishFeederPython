from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import Window_2
import sqlite3
import signal
import time
import sys
import threading
import subprocess



def motor_control():
    def return_main_frame():
        window.destroy()
        subprocess.call("Main_Frame.py", shell=True)
    def choose_analog():
        conn = sqlite3.connect('Value_holder.db')
        c = conn.cursor()
        c.execute("""UPDATE addresses SET
                                speed_control_method = :speed_control_method

                                WHERE oid = :oid""",
                                {
                                'speed_control_method': "Analog Input",
                                'oid': "1"
                                    })
        conn.commit()
        conn.close()
        window.destroy()
        subprocess.call("Main_Frame.py", shell=True)
    def choose_pwm():
        conn = sqlite3.connect('Value_holder.db')
        c = conn.cursor()
        c.execute("""UPDATE addresses SET
                                speed_control_method = :speed_control_method

                                WHERE oid = :oid""",
                                {
                                'speed_control_method': "PWM",
                                'oid': "1"
                                    })
        conn.commit()
        conn.close()
        window.destroy()
        subprocess.call("Main_Frame.py", shell=True)
    window = Tk()
    window.title("Motor Control")
    window.geometry("400x200")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=400, height=200, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

    #TEXTS
    my_canvas.create_text(200, 20, text="SELECT MOTOR SPEED CONTROL METHOD", font=("Helvetica", 11), fill="white")

     #BUTTONS
    analog_input_button = Button(window, text = "ANALOG INPUT" + "\n" + " (POTENTIO-SERVO COUPLING)", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 10, pady = 35, command=choose_analog)
    pulse_width_modulation_button = Button(window, text = "PULSE WIDTH" + "\n" + "MODULATION", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 53, pady = 35, command=choose_pwm)
    close_button = Button(window, text = "CANCEL", font="Helvetica 8 bold", fg="white", bg="red", padx = 18, pady = 10, command=return_main_frame)

    analog_input_window = my_canvas.create_window(5, 40, anchor="nw", window=analog_input_button)
    pulse_width_modulation_window = my_canvas.create_window(205, 40, anchor="nw", window=pulse_width_modulation_button)
    close_window = my_canvas.create_window(300, 150, anchor="nw", window=close_button)
    
    window.mainloop()


def schedule():
    global schedule_listbox
    global daily_schedule_listbox

    def edit_profile():
        try:
            list_id = str(schedule_listbox.index(ANCHOR) + 1)
            window.destroy()
            Window_2.schedule_edit(list_id)
        except:
            Window_2.warning_invalid_value()
    def apply_profile():
        try:
            list_id = str(schedule_listbox.index(ANCHOR) + 1)
            
            conn = sqlite3.connect('Value_holder.db')
            c = conn.cursor()
            c.execute("SELECT * FROM profiles WHERE oid=" + list_id)
            items = c.fetchall()
                    
            for item in items:
                schedule_name = str(item[0])
                species = str(item[1])
                estimated_population = str(item[2])
                feed_name = str(item[3])
                dfa = str(item[4])
                dfa_update_period = str(item[5])
                feed_increment = str(item[6])
                
            conn.commit()
            conn.close()

            conn = sqlite3.connect('Value_holder.db')
            c = conn.cursor()
            c.execute("""UPDATE addresses SET
                                    schedule_name = :schedule_name,
                                    species = :species,
                                    estimated_population = :estimated_population,
                                    feed_name = :feed_name,
                                    dfa = :dfa,
                                    dfa_update_period = :dfa_update_period,
                                    feed_increment = :feed_increment

                                    WHERE oid = :oid""",
                                    {
                                    'schedule_name': schedule_name,
                                    'species': species,
                                    'estimated_population': estimated_population,
                                    'feed_name': feed_name,
                                    'dfa': float(dfa),
                                    'dfa_update_period': int(dfa_update_period),
                                    'feed_increment': float(feed_increment),
                                    'oid': "1"
                                    })
            conn.commit()
            conn.close()
            window.destroy()
            subprocess.call("Main_Frame.py", shell=True)
        except:
            Window_2.warning_invalid_value()
        
    def return_main_frame():
        window.destroy()
        subprocess.call("Main_Frame.py", shell=True)
    def add_profile():
        window.destroy()
        Window_2.schedule_add()
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
    def fill_profiles_listbox():
        schedule_listbox.delete(0, END)
        conn = sqlite3.connect('Value_holder.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM profiles")
        items = c.fetchall()
                
        for item in items:
            schedule_listbox.insert (END, str(item[0]) + "///" +str(item[1]) + "///" + str(item[2]) + "///" + str(item[3]) +  "///" + str(item[4]) +"kg" +  "///" + str(item[5]) + "days" +  "///" + str(item[6]) + "kg")
        conn.commit()
        conn.close()
        
    def delete_profile():

        list_id = str(schedule_listbox.index(ANCHOR) + 1)
        conn = sqlite3.connect('Value_holder.db')
        c = conn.cursor()

        c.execute("DELETE from profiles WHERE oid=" + list_id)
        conn.commit()
        conn.close()
        fill_profiles_listbox()

    def submit_date():
        try:
            if int(hour_entry.get()) > 23 or int(minute_entry.get()) > 59:
                Window_2.warning_invalid_value()
            else:
                conn = sqlite3.connect('Value_holder.db')
                c = conn.cursor()

                c.execute("INSERT INTO daily_schedules VALUES (:hour, :minute)",
                    {
                        'hour': hour_entry.get(),
                        'minute': minute_entry.get()
                     })
                conn.commit()
                conn.close()
    
                fill_daily_schedule_listbox()
                hour_entry.delete(0, END)
                minute_entry.delete(0, END)
        except:
            Window_2.warning_invalid_value()
    def delete_date():

        list_id = str(daily_schedule_listbox.index(ANCHOR) + 1)
        conn = sqlite3.connect('Value_holder.db')
        c = conn.cursor()

        c.execute("DELETE from daily_schedules WHERE oid=" + list_id)
        conn.commit()
        conn.close()
        fill_daily_schedule_listbox()

        
    window = Tk()
    window.title("Shedule")
    window.geometry("800x450")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=800, height=450, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

    #TEXTS
    my_canvas.create_text(70, 20, text="PROFILE LIST", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(600, 60, text="Daily Feeding Schedule", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(553, 283, text="HOUR (0~23)", font=("Helvetica", 7), fill="white")
    my_canvas.create_text(683, 283, text="MINUTE (0~59)", font=("Helvetica", 7), fill="white")

    #ENTRY
    hour_entry = Entry(window, font="none 11 bold", width=14, borderwidth=2, bg="white")
    minute_entry = Entry(window, font="none 11 bold", width=14, borderwidth=2, bg="white")

    hour_window = my_canvas.create_window(525, 290, anchor="nw", window=hour_entry)
    minute_window = my_canvas.create_window(650, 290, anchor="nw", window=minute_entry)
    
   #LISTBOX
    schedule_listbox = Listbox(window, font="Helvetica 8 bold", fg="white", bg="gray", height = 22, width = 75)
    daily_schedule_listbox = Listbox(window, font="Helvetica 11 bold", fg="gray", bg="white", height = 10, width = 30)
    
    schedule_window = my_canvas.create_window(10, 40, anchor="nw", window=schedule_listbox)
    daily_schedule_window = my_canvas.create_window(525, 80, anchor="nw", window=daily_schedule_listbox)
    

    #BUTTONS
    add_schedule_button = Button(window, text = "ADD", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 32, pady = 12, command=add_profile)
    apply_schedule_button = Button(window, text = "APPLY", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 25, pady = 12, command =apply_profile)
    edit_schedule_button = Button(window, text = "EDIT", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 30, pady = 12, command=edit_profile)
    delete_schedule_button = Button(window, text = "DELETE", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 24, pady = 12, command=delete_profile)
    close_schedule_button = Button(window, text = "RETURN", font="Helvetica 8 bold", fg="white", bg="red", padx = 24, pady = 12, command=return_main_frame)
    add_daily_schedule_button = Button(window, text = "SUBMIT", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 4, pady = 5, command = submit_date)
    delete_daily_schedule_button = Button(window, text = "DELETE", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 4, pady = 5, command = delete_date)
  

    add_schedule_window = my_canvas.create_window(10, 395, anchor="nw", window=add_schedule_button)
    apply_schedule_window = my_canvas.create_window(110, 395, anchor="nw", window=apply_schedule_button)
    edit_schedule_window = my_canvas.create_window(210, 395, anchor="nw", window=edit_schedule_button)
    delete_schedule_window = my_canvas.create_window(307, 395, anchor="nw", window=delete_schedule_button)
    close_schedule_window = my_canvas.create_window(690, 395, anchor="nw", window=close_schedule_button)
    add_daily_schedule_window = my_canvas.create_window(525, 320, anchor="nw", window=add_daily_schedule_button)
    delete_daily_schedule_window = my_canvas.create_window(589, 320, anchor="nw", window=delete_daily_schedule_button)

    fill_profiles_listbox()
    fill_daily_schedule_listbox()
    
    window.mainloop()


def manual_override():

    def return_main_frame():
        window.destroy()
        subprocess.call("Main_Frame.py", shell=True)
        
    window = Tk()
    window.title("Manual Over Ride")
    window.geometry("800x450")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=800, height=450, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

    #TEXTS
    my_canvas.create_text(200, 20, text="ANALOG INPUT CONTROL", font=("Helvetica", 11), fill="white")
    
    #FIXED LINES
    #horizontal
    my_canvas.create_line(0, 320, 800, 320, fill="gray")
    
    #vertical
    my_canvas.create_line(400, 0, 400, 320, fill="gray")
    
    #BUTTONS
    close_schedule_button = Button(window, text = "RETURN", font="Helvetica 8 bold", fg="white", bg="red", padx = 24, pady = 12, command=return_main_frame)
    energize_motor1_button = Button(window, text = "ENERGIZE MOTOR 1", font="Helvetica 8 bold", fg="white", bg="green", padx = 20, pady = 12)
    de_energize_motor1_button = Button(window, text = "DE-ENERGIZE MOTOR 1", font="Helvetica 8 bold", fg="white", bg="red", padx = 16, pady = 12)
    energize_motor2_button = Button(window, text = "ENERGIZE MOTOR 2", font="Helvetica 8 bold", fg="white", bg="green", padx = 20, pady = 12)
    de_energize_motor2_button = Button(window, text = "DE-ENERGIZE MOTOR 2", font="Helvetica 8 bold", fg="white", bg="red", padx = 16, pady = 12)

    close_schedule_window = my_canvas.create_window(690, 395, anchor="nw", window=close_schedule_button)
    energize_motor1_window = my_canvas.create_window(30, 70, anchor="nw", window=energize_motor1_button)
    de_energize_motor1_window = my_canvas.create_window(217, 70, anchor="nw", window=de_energize_motor1_button)
    energize_motor2_window = my_canvas.create_window(30, 250, anchor="nw", window=energize_motor2_button)
    de_energize_motor2_window = my_canvas.create_window(217, 250, anchor="nw", window=de_energize_motor2_button)

    #SLIDER
    my_scale = Scale(window, from_ = 0, to = 100, orient = HORIZONTAL, length = 338, bg="gray")
    my_scale_window = my_canvas.create_window(30, 145, anchor="nw", window=my_scale)

    window.mainloop()


def calibration():
    window = Tk()
    window.title("Calibration")
    window.geometry("800x450")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=800, height=450, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

   
    window.mainloop()


def information():
    window = Tk()
    window.title("Information")
    window.geometry("800x450")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=800, height=450, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

   
    window.mainloop()

def options():
    window = Tk()
    window.title("Options")
    window.geometry("800x450")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=800, height=450, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

   
    window.mainloop()


