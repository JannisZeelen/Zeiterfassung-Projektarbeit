import tkinter as tk
from tkinter import ttk
from datetime import datetime as dt, timedelta as td
import csv
import matplotlib.pyplot as plt
import sv_ttk

file = 'zeiterfassung.csv'


# ======= datetime functions =======
def get_date():
    current_datetime = dt.now()
    return current_datetime.strftime("%d.%m.%Y")


def get_time():
    current_datetime = dt.now()
    current_time = current_datetime.strftime("%H:%M:%S")
    label_time.config(text=current_time)
    root.after(1000, get_time)
    return current_time


def get_worktime_float(time):
    formatted_time = dt.strptime(time, "%H:%M:%S")
    total_seconds = td(hours=formatted_time.hour, minutes=formatted_time.minute,
                       seconds=formatted_time.second).total_seconds()
    worktime_float = total_seconds / 3600.0
    return worktime_float


# ======= button functions =======
def check_in():
    print(f"Checking you in!")
    button_check_in["state"] = "disabled"
    button_check_out["state"] = "active"
    csv_write_check_in()


def check_out():
    print(f"Checking you out!")
    button_check_out["state"] = "disabled"
    button_check_in["state"] = "active"
    csv_write_check_out()


def user_quit():
    root.quit()


# ======= .csv functions =======
def get_status():
    with open(file, 'r', newline='') as csv_file:
        existing_data = list(csv.reader(csv_file))

        if existing_data and len(existing_data[-1]) == 2:
            button_check_in["text"] = "You are checked in."
            return True


def csv_write_check_in():
    with open(file, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([get_date(), get_time()])
    print('Zeiten wurden gespeichert')


def csv_write_check_out():
    with open(file, 'r+', newline='') as csv_file:
        existing_data = list(csv.reader(csv_file))

        if existing_data and len(existing_data[-1]) == 2:
            check_in_time = dt.strptime(existing_data[-1][1], "%H:%M:%S")
            check_out_time = dt.strptime(get_time(), "%H:%M:%S")

            timedelta = check_out_time - check_in_time
            base_date = dt(1900, 1, 1)
            worktime = base_date + timedelta
            print(worktime)
            # worktime_float = get_worktime_float(worktime.strftime("%H:%M:%S"))
            existing_data[-1].extend([get_time(), worktime.strftime("%H:%M:%S")])

            # Move the file cursor to the beginning to overwrite the existing data
            csv_file.seek(0)
            csv_writer = csv.writer(csv_file)

            # Write the modified data back to the file
            csv_writer.writerows(existing_data)

    print('Zeiten wurden gespeichert')


def show_plot():
    # TODO: Funktion derzeit: Bar plot der letzten 5 tage float stunden arbeitszeit. / andere ideen besser?
    with open('zeiterfassung.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)[-5:]

    work_hours = []
    days = []

    for row in rows:
        work_hours.append(get_worktime_float(row[3]))
        days.append(row[0])

    # work_hours.reverse()
    # days.reverse()

    plt.bar(days, work_hours, color='skyblue')
    plt.xlabel('Wochentag')
    plt.ylabel('Arbeitsstunden')
    plt.title('Arbeitszeiten letzte 5 Tage')
    plt.show()


current_date = get_date()

root = tk.Tk()  # Fensternamme / Objekt

root.title('Zeiterfassung')
frame = ttk.Frame()

# styling ttk
style = ttk.Style()
sv_ttk.set_theme("dark")

# Date and Time Labels
label_top = ttk.Label(root, text='Hallo, Jannis!', style='TLabel')  # TODO: maybe with var in future with user model
label_top.grid(row=0, column=0, columnspan=2, sticky='nsew')

label_date = ttk.Label(root, text=current_date, font=('Helvetica', 16))
label_date.grid(row=1, column=0)

label_time = ttk.Label(root, font=('Helvetica', 16))
label_time.grid(row=1, column=1)

get_time()

button_check_in = ttk.Button(text='Check in', command=check_in, state="disabled")
if not get_status():
    button_check_in['state'] = "normal"
button_check_out = ttk.Button(text='Check out', command=check_out, state="disabled")
if get_status():
    button_check_out['state'] = "normal"

button_plot = ttk.Button(text='Show working times', command=show_plot)
button_user_quit = ttk.Button(text='Quit', command=user_quit)

button_plot.grid(row=2, column=0, columnspan=2, sticky='nsew')
button_check_in.grid(row=3, column=0, columnspan=2, sticky='nsew')
button_check_out.grid(row=4, column=0, columnspan=2, sticky='nsew')
button_user_quit.grid(row=5, column=0, columnspan=2, sticky='nsew')

for i in range(2):
    root.columnconfigure(i, weight=1)

root.geometry("500x300+1000+500")

root.mainloop()  # Eventloop starten

# TODO: Kommentare einsprachig ( deutsch für präsi )
# TODO: Wenn Arbeitszeit über x dann Pause abziehen
# TODO: Tkinter schöner machen
# TODO: CSV über matplotlib ausgeben
# TODO make connection to github
# TODO Pause button und abziehen von delta
# TODO Bild von alfa logo
# TODO alles auf ttk ändern
# TODO Berechnung von timedelta mit tagen einbeziehen sonst bei über 24h von null
# TODO Project vorstellen: 15 Minuten Zeit
