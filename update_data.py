import data_req
import schedule
import mydate_sql0
import time

def update_all_sql():
    dict = {'m1':'prof', 'm2':'doors', 'm2_1': 'doors', 'm3': 'event', 'm5':'olimpiads'}

    for tape in dict:
        m = data_req.Manager(tape, mydate_sql0.sql_manager(dict[tape]))
        m.manager(1, 0)

def main():
    schedule.every().day.at("07:00").do(update_all_sql)
    while True:
        schedule.run_pending()
        time.sleep(5)
    #update_all_sql()

if __name__ == "__main__":
    update_all_sql()
else:
    main()
