import tkinter as tk
from datetime import datetime as dt
from datetime import timedelta as td
import csv

file = 'zeiterfassung.csv'


# Datetime functions

def get_date():
    current_datetime = dt.now()
    return current_datetime.strftime("%d.%m.%Y")


def get_time():
    current_datetime = dt.now()
    current_time = current_datetime.strftime("%H:%M:%S")
    label_time.config(text=current_time)
    root.after(1000, get_time)
    return current_time


# Button Functions

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
    # function call / function to write in csv TODO


def user_quit():
    root.quit()


# def getinput():
#     print(f"Hallo, {input1.get()}!")
#     root.quit()  TODO Use this for a note to add when checking out

# .csv functions

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

            existing_data[-1].extend([get_time(), worktime.strftime("%H:%M:%S")])

            # Move the file cursor to the beginning to overwrite the existing data
            csv_file.seek(0)
            csv_writer = csv.writer(csv_file)

            # Write the modified data back to the file
            csv_writer.writerows(existing_data)

    print('Zeiten wurden gespeichert')


current_date = get_date()  # Call get_date to get the current date

root = tk.Tk()  # Fensternamme / Objekt
frame = tk.Frame()
# Date and Time Labels
label_top = tk.Label(root, text='Hallo, Jannis')  # TODO: maybe with var in future with user model
label_top.grid(row=0, column=0, columnspan=2, sticky='nsew')

label_date = tk.Label(root, text=current_date)
label_date.grid(row=1, column=0)

label_time = tk.Label(root, text="")
label_time.grid(row=1, column=1)

get_time()

button_check_in = tk.Button(text='Check in', command=check_in)
button_check_out = tk.Button(text='Check out', command=check_out)
button_user_quit = tk.Button(text='Quit', command=user_quit)
button_check_in.grid(row=2, column=0, columnspan=2, sticky='nsew')
button_check_out.grid(row=3, column=0, columnspan=2, sticky='nsew')
button_user_quit.grid(row=4, column=0, columnspan=2, sticky='nswe')
root.geometry("+1000+500")

root.mainloop()  # Eventloop starten

# TODO: Kommentare einsprachig
