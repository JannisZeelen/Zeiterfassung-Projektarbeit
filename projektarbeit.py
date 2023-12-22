import tkinter as tk
from tkinter import ttk
from datetime import datetime as dt, timedelta as td
import csv
import matplotlib.pyplot as plt
import sv_ttk

# Dateipfad für die Zeiterfassungsdaten
file = 'zeiterfassung.csv'


# ======= Datetime Funktionen =======
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
    # FFunktion, um die Arbeitszeit in Stunden als Float zu erhalten
    formatted_time = dt.strptime(time, "%H:%M:%S")
    total_seconds = td(hours=formatted_time.hour, minutes=formatted_time.minute,
                       seconds=formatted_time.second).total_seconds()
    worktime_float = total_seconds / 3600.0
    return worktime_float


# ======= Button-Funktionen =======
def check_in():
    # Check-in Button deaktivieren, Check-out Button aktivieren, Aufrufen von Check-in Funktion
    print(f"Checking you in!")  # TODO remove this?
    button_check_in["state"] = "disabled"
    button_check_out["state"] = "active"
    csv_write_check_in()


def check_out():
    # Check-out Button deaktivieren, Check-in Button aktivieren, Aufrufen von Check-out Funktion
    print(f"Checking you out!")
    button_check_out["state"] = "disabled"
    button_check_in["state"] = "active"
    csv_write_check_out()


def user_quit():
    # Tkinter schließen
    root.quit()


# ======= .csv Funktionen =======
def get_status():
    # Überprüfung, ob bereits eingecheckt worden ist, dementsprechene Button De-/Aktivierung
    with open(file, 'r', newline='') as csv_file:
        existing_data = list(csv.reader(csv_file))

        if existing_data and len(existing_data[-1]) == 2:
            button_check_in["text"] = "You are checked in."
            return True


def csv_write_check_in():
    # Datum + Check-in Zeit in neue Zeile schreiben
    with open(file, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([get_date(), get_time()])
    print('Zeiten wurden gespeichert')


def csv_write_check_out():
    # Check-out Zeit + Arbeitszeit in bestehende Zeile schreiben
    with open(file, 'r+', newline='') as csv_file:
        # Bestehende Daten in Variable zwischenspeichern
        existing_data = list(csv.reader(csv_file))

        # Überprüfung, ob bereits eingecheckt worde, falls ja Check-in Zeit speichern
        if existing_data and len(existing_data[-1]) == 2:
            check_in_time = dt.strptime(existing_data[-1][1], "%H:%M:%S")
            check_out_time = dt.strptime(get_time(), "%H:%M:%S")

            # Berechne die Arbeitszeit für den aktuellen Tag
            base_date = dt(1900, 1, 1)
            timedelta = check_out_time - check_in_time
            worktime = base_date + timedelta

            # Erweitern der Check-out und Arbeitszeit
            existing_data[-1].extend([get_time(), worktime.strftime("%H:%M:%S")])

            # An Beginn der Datei springen und neue Daten schreiben
            csv_file.seek(0)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(existing_data)

    print('Zeiten wurden gespeichert')


def create_plot(work_hours, last_5_days, last_5_days_no_year):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Bar Plot
    ax1.bar(last_5_days_no_year, work_hours, color='skyblue')
    ax1.set_xlabel('Wochentag')
    ax1.set_ylabel('Gesamtarbeitsstunden')
    ax1.set_title('Arbeitszeiten der letzten 5 Tage')

    # Pie Plot in %
    ax2.pie(work_hours, labels=last_5_days, autopct='%1.1f%%', startangle=90,
            colors=['skyblue', 'lightcoral', 'lightgreen', 'gold', 'lightpink'])
    ax2.set_title('Aufteilung Arbeitszeiten letzten 5 Tage')
    plt.tight_layout()


def math_plot():
    # TODO: Funktion derzeit: Bar plot der letzten 5 tage float stunden arbeitszeit. / andere ideen besser? mehrere plots
    with open('zeiterfassung.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    # Leeres Dictionary für zukünftige Date:Worktime Werte
    work_hours_per_day = {}

    # Datum und Arbeitszeit in Listen speichern
    for row in rows[1:]:
        date = row[0]
        work_hours = get_worktime_float(row[3])

        # Wenn der Tag bereits im Dictionary ist, addiere die Arbeitszeit
        if date in work_hours_per_day:
            work_hours_per_day[date] += work_hours
        else:
            work_hours_per_day[date] = work_hours

    # Bereitstellen von Listen für die Ploterstellung
    last_5_days = list(work_hours_per_day.keys())[-5:]
    last_5_days_no_year = [day[:-4] for day in last_5_days]
    work_hours = [work_hours_per_day[day] for day in last_5_days]

    # Funktion zum Erstellen der Plots aufrufen
    create_plot(work_hours, last_5_days, last_5_days_no_year)

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

button_plot = ttk.Button(text='Show working times', command=math_plot)
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
# TODO Project vorstellen: 15 Minuten Zeit
# TODO überprüfung wenn erst am nächsten tag ausgecheckt wird(vorheriger tag bis 24 dann neuer eintrag?
# TODO Alles erklären könnnen
