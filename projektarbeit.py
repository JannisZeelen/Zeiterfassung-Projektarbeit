import locale
import tkinter as tk
from tkinter import ttk
from datetime import datetime as dt, timedelta as td
import csv
import matplotlib.pyplot as plt
import sv_ttk

locale.setlocale(locale.LC_TIME, 'de_DE')

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


# ======= ttkinter-Funktionen =======
def check_in():
    # Überprüft den aktuellen Status bei Check-in/Check-out und ruft die jeweilige Funktion zum Schreiben auf
    if not get_status():
        button_check_in.config(text='Check-out')
        csv_write_check_in()
        print(f"Checking you in!")
    else:
        button_check_in.config(text='Check-in')
        csv_write_check_out()
        print(f"Checking you out!")


def user_quit():
    # Tkinter schließen
    root.quit()


def highlight_clear(event):
    current = dropdown_month.get()
    dropdown_month.set('')
    dropdown_month.set(current)


# ======= .csv Funktionen =======
def get_status():
    # Überprüfung, ob bereits eingecheckt worden ist, returns Bool
    with open(file, 'r', newline='') as csv_file:
        existing_data = list(csv.reader(csv_file))

        if existing_data and len(existing_data[-1]) == 2:
            return True
        else:
            return False


def get_worked_months():
    with open('zeiterfassung.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    worked_months_year = []
    for row in rows[1:]:
        month_year = row[0][3:]
        if month_year in worked_months_year:
            pass
        else:
            worked_months_year.append(month_year)
    formatted = []
    for month in worked_months_year:
        formatted.append(dt.strptime(month, '%m.%Y').strftime('%B %Y'))
    formatted.reverse()
    return formatted


def csv_write_check_in():
    # Datum + Check-in Zeit in neue Zeile schreiben
    with open(file, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([get_date(), get_time()])


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


#     # Pie Plot in %
#     ax2.pie(work_hours, labels=last_5_days, autopct='%1.1f%%', startangle=90,
#             colors=['skyblue', 'lightcoral', 'lightgreen', 'gold', 'lightpink'])
#     ax2.set_title('Aufteilung Arbeitszeiten letzten 5 Tage')
#     plt.tight_layout()


def create_plot(work_hours, last_days, last_days_no_year, plot_title):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Bar Plot
    ax.bar(last_days_no_year, work_hours, color='skyblue')

    average_work_hours = sum(work_hours) / len(work_hours)
    ax.axhline(y=average_work_hours, color='red', linestyle='--', label='Durchschnitt')

    ax.set_xlabel('Datum')
    ax.set_ylabel('Gesamtarbeitsstunden')
    ax.set_title(plot_title)
    plt.xticks(rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()


def math_plot():
    # Funktion zur Berechnung der Arbeitsstunden, Auslesen der Reihen mit dem gleichen Monat
    with open('zeiterfassung.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    # Leeres Dictionary für zukünftige Date:Worktime Werte
    work_hours_per_day = {}

    # Datum und Arbeitszeit in Listen speichern
    for row in rows[1:]:
        if len(row) >=4:
            date = row[0]
            work_hours = get_worktime_float(row[3])

            # Wenn der Tag im gewünschten Monat und Jahr ist, addiere die Arbeitszeit
            if date.endswith(dt.strptime(dropdown_month.get(), '%B %Y').strftime('%m.%Y')):
                if date in work_hours_per_day:
                    work_hours_per_day[date] += work_hours
                else:
                    work_hours_per_day[date] = work_hours

    # Bereitstellen von Listen für die Ploterstellung
    last_days = list(work_hours_per_day.keys())
    last_days_no_year = [day[:-4] for day in last_days]
    work_hours = [work_hours_per_day[day] for day in last_days]

    # Funktion zum Erstellen der Plots aufrufen
    create_plot(work_hours, last_days, last_days_no_year, f'Arbeitszeiten {dropdown_month.get()}')

    plt.show()


current_date = get_date()

# Create main Tkinter window
root = tk.Tk()
root.title('Zeiterfassung')

# Create frames with borders
frame_0_0 = tk.Frame(root, highlightbackground='blue', highlightthickness=2, padx=15, pady=5, borderwidth=15)
frame_1_0 = tk.Frame(root, highlightbackground='blue', highlightthickness=2, padx=15, pady=5, borderwidth=15)
frame_0_1 = tk.Frame(root, highlightbackground='blue', highlightthickness=2, padx=15, pady=5, borderwidth=15)
frame_1_1 = tk.Frame(root, highlightbackground='blue', highlightthickness=2, padx=15, pady=5, borderwidth=15)

# Styling for ttk
style = ttk.Style()
sv_ttk.set_theme("dark")
style.configure('TFrame')

# Date and Time Labels
label_hello = ttk.Label(frame_0_0, text='Hallo, Jannis!', anchor="center", justify="center")
label_placeholder = ttk.Label(frame_1_1, text='Placeholder', anchor="center", justify="center")
label_timetracking = ttk.Label(frame_1_0, text='Zeiterfassung', anchor="center", justify="center")
label_space = ttk.Label(frame_0_0, text='-------------', anchor="center", justify="center")

label_date = ttk.Label(frame_0_0, text=current_date, anchor='center', justify='center')
label_time = ttk.Label(frame_0_0, anchor='center', justify='center')

# Buttons and Combobox
get_time()
worked_months = get_worked_months()
button_check_in = ttk.Button(frame_1_0, text='Check-in', command=check_in, compound="center")
if get_status():
    button_check_in.config(text='Check-out')
button_plot = ttk.Button(frame_0_1, text='Arbeitszeit aufrufen', command=math_plot)
button_user_quit = ttk.Button(text='Quit', command=user_quit)

dropdown_month = ttk.Combobox(frame_0_1, values=worked_months, state='readonly')
dropdown_month.current(0)
dropdown_month.bind("<<ComboboxSelected>>", highlight_clear)

# Grid placement
frame_0_0.grid(row=0, column=0, pady=15, padx=15, sticky='nsew')
frame_0_0.grid_columnconfigure(0, weight=1)
frame_1_0.grid(row=1, column=0, pady=15, padx=15, sticky='nsew')
frame_0_1.grid(row=0, column=1, pady=15, padx=15, sticky='nsew')
frame_1_1.grid(row=1, column=1, pady=15, padx=15, sticky='nsew')
label_hello.grid(row=0, column=0, sticky='nsew')
label_placeholder.grid(row=0, column=0, sticky='nsew')
label_space.grid(row=1, column=0, sticky='nsew')
label_timetracking.grid(row=1, column=0, sticky='nsew')
label_date.grid(row=2, column=0, sticky='nsew')
label_time.grid(row=3, column=0, sticky='nsew')
button_plot.grid(row=3, column=1, sticky='nsew', pady=5)
button_check_in.grid(row=2, column=0, sticky='nsew', pady=5)
button_user_quit.grid(row=5, column=0, columnspan=2)
dropdown_month.grid(row=0, column=1)

# Configure column weights
for i in range(6):
    root.columnconfigure(i, weight=1)

# Set window geometry
root.geometry("472x330+1000+500")

# Start the Tkinter event loop
root.mainloop()

# TODO: Kommentare einsprachig ( deutsch für präsi )
# TODO: Wenn Arbeitszeit über x dann Pause abziehen
# TODO: Pause als zweiten Balken ins Matplotlib
# TODO: Pause Button
# TODO: Tkinter schöner machen
# TODO Bild von alfa logo??
# TODO Project vorstellen: 15 Minuten Zeit
# TODO überprüfung wenn erst am nächsten tag ausgecheckt wird(vorheriger tag bis 24 dann neuer eintrag?
# TODO Alles erklären könnnen
# TODO Focus entfernen von geklickten Buttons
