import sqlite3

def get_value_holder():
    conn = sqlite3.connect('Value_holder.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    items = c.fetchall()
    
    for item in items:
        schedule_name = str(item[0])
        species = str(item[1])
        estimated_population = str(item[2])
        feed_name = str(item[3])
        dfa = str(item[4])
        dfa_update_period = str(item[5])
        feed_increment = str(item[6])
        speed_control_method = str(item[7])
            
    conn.commit()
    conn.close()
    return schedule_name, species, estimated_population, feed_name, dfa, dfa_update_period, feed_increment, speed_control_method


    
