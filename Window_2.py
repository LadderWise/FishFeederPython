from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import Window_1
import sqlite3
import signal
import time
import sys
import threading

def warning_invalid_value():
    window = Tk()
    window.title("WARNING!")
    window.geometry("400x150")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=600, height=200, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

    #TEXTS
    my_canvas.create_text(200, 40, text="WARNING! INVALID INPUT.", font=("Helvetica", 18), fill="red")

    #BUTTONS
    close_button = Button(window, text = "OKAY", font="Helvetica 15 bold", fg="white", bg="#444343", padx = 55, pady = 15, command=lambda:window.destroy())

    close_window = my_canvas.create_window(117, 65, anchor="nw", window=close_button)

    window.mainloop()

def schedule_add():
    def close_profile():
        window.destroy()
        Window_1.schedule()
    def save_profile():
        try:
            if len(schedule_name_entry.get())<1 or len(species_entry.get())<1 or len(estimated_population_entry .get())<1 or len(feed_name_entry.get())<1 or len(dfa_entry.get())<1 or len(dfa_update_period_entry.get())<1 or len(feed_increment_entry.get())<1:
                warning_invalid_value()
            else:
                conn = sqlite3.connect('Value_holder.db')
                c = conn.cursor()

                c.execute("INSERT INTO profiles VALUES (:schedule_name, :species, :estimated_population, :feed_name, :dfa, :dfa_update_period, :feed_increment)",
                    {
                        'schedule_name':schedule_name_entry.get(),
                        'species':species_entry.get(),
                        'estimated_population':estimated_population_entry .get(),
                        'feed_name':feed_name_entry.get(),
                        'dfa':float(dfa_entry.get()),
                        'dfa_update_period':int(dfa_update_period_entry.get()),
                        'feed_increment':float(feed_increment_entry.get())
                    })
                conn.commit()
                conn.close()

                window.destroy()
                Window_1.schedule()
                
        except:
            warning_invalid_value()
            
    window = Tk()
    window.title("Add Schedule")
    window.geometry("800x450")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=800, height=450, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

    #TEXTS
    my_canvas.create_text(180, 20, text="FILL UP EACH INFORMATION REQUIREMENT", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(92, 60, text="Schedule Name", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(117, 100, text="Species", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(96, 140, text="Est. Population", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(106, 180, text="Feed Name", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(75, 220, text="Daily Feed Allowance", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(83, 260, text="DFA Update Period", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(94, 300, text="Feed Increment", font=("Helvetica", 11), fill="white")

   
    #ENTRY
    schedule_name_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    species_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    estimated_population_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    feed_name_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    dfa_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    dfa_update_period_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    feed_increment_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")

    
    schedule_entry_window = my_canvas.create_window(170, 50, anchor="nw", window=schedule_name_entry)
    species_window = my_canvas.create_window(170, 90, anchor="nw", window=species_entry)
    estimated_population_window = my_canvas.create_window(170, 130, anchor="nw", window=estimated_population_entry)
    feed_name_window = my_canvas.create_window(170, 170, anchor="nw", window=feed_name_entry)
    dfa_window = my_canvas.create_window(170, 210, anchor="nw", window=dfa_entry)
    dfa_update_period_window = my_canvas.create_window(170, 250, anchor="nw", window=dfa_update_period_entry)
    feed_increment_window = my_canvas.create_window(170, 290, anchor="nw", window=feed_increment_entry)


    #BUTTONS
    close_schedule_button = Button(window, text = "CLOSE", font="Helvetica 8 bold", fg="white", bg="red", padx = 24, pady = 12, command=close_profile)
    save_schedule_button = Button(window, text = "SAVE", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 25, pady = 12, command = save_profile)
    
    close_schedule_window = my_canvas.create_window(690, 395, anchor="nw", window=close_schedule_button)
    save_schedule_window = my_canvas.create_window(10, 395, anchor="nw", window=save_schedule_button)

   
    window.mainloop()


def schedule_edit(index):
    def close_profile():
        window.destroy()
        Window_1.schedule()
    def save_profile():
        try:
            if len(schedule_name_entry.get())<1 or len(species_entry.get())<1 or len(estimated_population_entry .get())<1 or len(feed_name_entry.get())<1 or len(dfa_entry.get())<1 or len(dfa_update_period_entry.get())<1 or len(feed_increment_entry.get())<1:
                warning_invalid_value()
            else:


                conn = sqlite3.connect('Value_holder.db')
                c = conn.cursor()
                c.execute("""UPDATE profiles SET
                                        schedule_name = :schedule_name,
                                        species = :species,
                                        estimated_population = :estimated_population,
                                        feed_name = :feed_name,
                                        dfa = :dfa,
                                        dfa_update_period = :dfa_update_period,
                                        feed_increment = :feed_increment

                                        WHERE oid = :oid""",
                                        {
                                        'schedule_name': schedule_name_entry.get(),
                                        'species': species_entry.get(),
                                        'estimated_population': estimated_population_entry.get(),
                                        'feed_name': feed_name_entry.get(),
                                        'dfa': float(dfa_entry.get()),
                                        'dfa_update_period': int(dfa_update_period_entry.get()),
                                        'feed_increment': float(feed_increment_entry.get()),
                                        'oid': str(index)
                                        })
                conn.commit()
                conn.close()

                window.destroy()
                Window_1.schedule()
                
        except:
            warning_invalid_value()
            
    window = Tk()
    window.title(" Edit Profile")
    window.geometry("800x450")
    window.resizable(0, 0)

    my_canvas = Canvas(window, width=800, height=450, bg="#262424")
    my_canvas.pack(fill="both", expand=False)

    #TEXTS
    my_canvas.create_text(180, 20, text="FILL UP EACH INFORMATION REQUIREMENT", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(92, 60, text="Schedule Name", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(117, 100, text="Species", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(96, 140, text="Est. Population", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(106, 180, text="Feed Name", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(75, 220, text="Daily Feed Allowance", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(83, 260, text="DFA Update Period", font=("Helvetica", 11), fill="white")
    my_canvas.create_text(94, 300, text="Feed Increment", font=("Helvetica", 11), fill="white")

   
    #ENTRY
    schedule_name_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    species_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    estimated_population_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    feed_name_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    dfa_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    dfa_update_period_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")
    feed_increment_entry = Entry(window, font="none 11 bold", width=35, borderwidth=2, bg="white")

    
    schedule_entry_window = my_canvas.create_window(170, 50, anchor="nw", window=schedule_name_entry)
    species_window = my_canvas.create_window(170, 90, anchor="nw", window=species_entry)
    estimated_population_window = my_canvas.create_window(170, 130, anchor="nw", window=estimated_population_entry)
    feed_name_window = my_canvas.create_window(170, 170, anchor="nw", window=feed_name_entry)
    dfa_window = my_canvas.create_window(170, 210, anchor="nw", window=dfa_entry)
    dfa_update_period_window = my_canvas.create_window(170, 250, anchor="nw", window=dfa_update_period_entry)
    feed_increment_window = my_canvas.create_window(170, 290, anchor="nw", window=feed_increment_entry)


    #BUTTONS
    close_schedule_button = Button(window, text = "CLOSE", font="Helvetica 8 bold", fg="white", bg="red", padx = 24, pady = 12, command=close_profile)
    save_schedule_button = Button(window, text = "UPDATE", font="Helvetica 8 bold", fg="white", bg="#444343", padx = 25, pady = 12, command = save_profile)
    
    close_schedule_window = my_canvas.create_window(690, 395, anchor="nw", window=close_schedule_button)
    save_schedule_window = my_canvas.create_window(10, 395, anchor="nw", window=save_schedule_button)

    conn = sqlite3.connect('Value_holder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM profiles WHERE oid=" + index)
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

    schedule_name_entry.insert(0, schedule_name)
    species_entry.insert(0, species)
    estimated_population_entry.insert(0, estimated_population)
    feed_name_entry.insert(0, feed_name)
    dfa_entry.insert(0, dfa)
    dfa_update_period_entry.insert(0, dfa_update_period)
    feed_increment_entry.insert(0, feed_increment)
   
    window.mainloop()
