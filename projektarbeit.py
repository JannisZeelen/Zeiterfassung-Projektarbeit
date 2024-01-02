import locale
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from datetime import datetime as dt, timedelta as td
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as tkagg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Deutsche Lokalisierung für Datumsformatierung
locale.setlocale(locale.LC_TIME, 'de_DE')

# Dateipfad für die Zeiterfassungsdaten
file = 'zeiterfassung.csv'


# ======= Datetime Funktionen =======
def get_date():
    current_dt = dt.now()
    return current_dt.strftime("%d.%m.%Y")


def get_time():
    current_dt = dt.now()
    current_time = current_dt.strftime("%H:%M:%S")
    label_time.config(text=current_time)
    root.after(1000, get_time)
    return current_time


def get_date_time():
    current_dt = dt.now()
    return current_dt


# ======= ttkinter-Funktionen =======
def check_in():
    # Überprüft den aktuellen Status bei Check-in/Check-out und ruft die jeweilige Funktion zum Schreiben auf
    if get_status():
        # Check-out Funktionen
        button_check_in.config(text='Check-in')
        csv_write_check_out()
        print(f"Checking you out!")
    else:
        # Check-in Funktionen
        button_check_in.config(text='Check-out')
        csv_write_check_in()
        print(f"Checking you in!")


def user_quit():
    # Tkinter schließen
    root.destroy()


def highlight_clear(event):
    # Funktion um neu ausgewähltes Dropdown Element als nicht markiert darzustellen
    current = dropdown_month.get()
    dropdown_month.set('')
    dropdown_month.set(current)


# ======= .csv Funktionen =======
def get_status():
    # Überprüfung, ob bereits eingecheckt worden ist, gibt einen Bool-Wert zurück

    # Öffne die CSV-Datei im Lese-Modus
    with open(file, 'r', newline='') as csv_file:
        # Lese alle vorhandenen Daten in eine Liste
        existing_data = list(csv.reader(csv_file))

        # Überprüfe, ob Daten vorhanden sind und ob die letzte Zeile nur ein Element hat
        if existing_data and len(existing_data[-1]) == 1:
            # Der Benutzer hat bereits eingecheckt
            return True
        else:
            # Der Benutzer hat noch nicht eingecheckt
            return False


def get_worked_months():  # TODO Kommentare
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    worked_months_year = set()
    for row in rows[:]:
        if len(row) == 3:
            date_time_str = row[0]
            try:
                date_time = dt.strptime(date_time_str, "%d.%m.%Y-%H:%M:%S")
                month_year = date_time.strftime('%m.%Y')
                worked_months_year.add(month_year)
            except ValueError:
                # Skip entries that do not match the expected format
                continue

    formatted = sorted([dt.strptime(month, '%m.%Y').strftime('%B %Y') for month in worked_months_year],
                       key=lambda x: dt.strptime(x, '%B %Y'), reverse=True)
    return formatted


def csv_write_check_in():
    # Check-in Datum und Zeit in neue Zeile schreiben
    with open(file, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([get_date_time().strftime("%d.%m.%Y-%H:%M:%S")])


def csv_write_check_out():
    # Check-out Zeit + Arbeitszeit in bestehende Zeile schreiben

    with open(file, 'r+', newline='') as csv_file:
        # Lese alle vorhandenen Daten in eine Liste
        existing_data = list(csv.reader(csv_file))

        # Überprüfung, ob bereits eingecheckt worden ist, falls ja Check-in Zeit und Datum speichern
        if existing_data and len(existing_data[-1]) == 1:
            check_in_dt_str = existing_data[-1][0]

            # Variablen für Check-in, Check-out
            check_in_dt = dt.strptime(check_in_dt_str, "%d.%m.%Y-%H:%M:%S")
            check_out_dt = get_date_time()
            check_out_dt_str = check_out_dt.strftime("%d.%m.%Y-%H:%M:%S")

            # Arbeitszeit als Differenz von Check-in und Check-out
            timedelta = check_out_dt - check_in_dt

            # Differenz in Sekunden umrechnen, dann in Stunden, Minuten und Sekunden aufteilen
            total_seconds = timedelta.total_seconds()
            worktime = total_seconds / 3600

        # Aktuelle Row in Kopie aktualisieren
        existing_data[-1] = [check_in_dt_str, check_out_dt_str, worktime]

        # An Beginn der Datei springen und neue Daten schreiben
        csv_file.seek(0)
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(existing_data)


def calculate_break_times():
    with open(file, 'r+', newline='') as csv_file:
        # Bestehende Daten in Variable zwischenspeichern
        existing_data = list(csv.reader(csv_file))
        prev_date = None
        break_times = {}
        for row in existing_data[1:]:
            # Nur abgeschlossene Arbeitszeiten
            if len(row) == 3:
                selected_month_year = dt.strptime(dropdown_month.get(), '%B %Y').strftime('%m.%Y')
                check_out_date_str = row[1]
                date_time = dt.strptime(check_out_date_str, "%d.%m.%Y-%H:%M:%S")
                check_out_date_str = date_time.strftime("%d.%m.%Y")

                # Wenn der gewünschte Monat Jahr übereinstimmt
                if check_out_date_str.endswith(selected_month_year):
                    # Setzen des aktuellen Datums in benötigten Formaten
                    curr_date = dt.strptime(row[0], "%d.%m.%Y-%H:%M:%S").strftime("%d.%m.%Y")
                    curr_check_in = dt.strptime(row[0], "%d.%m.%Y-%H:%M:%S")

                    # Wenn das Datum an zwei Tagen gleich ist, berechne die Pause
                    if prev_date == curr_date:
                        timedelta = curr_check_in - prev_check_out
                        timedelta = timedelta.total_seconds() / 3600

                        # Speichern in break_times Dictionary
                        break_times[curr_date] = timedelta
                    else:
                        break_times[curr_date] = 0

                    # Setzen des aktuellen Datums bevor der Schleifendurchlauf endet
                    prev_date = dt.strptime(row[0], "%d.%m.%Y-%H:%M:%S").strftime("%d.%m.%Y")
                    prev_check_out = dt.strptime(row[1], "%d.%m.%Y-%H:%M:%S")
        return break_times


def create_plot(work_hours, monthly_days, break_times, plot_title):
    # Monatsdaten ohne Jahr extrahieren
    monthly_days_no_year = [day[:-4] for day in monthly_days]

    # Figure- und Axes-Objekt erstellen
    fig, ax = plt.subplots(figsize=(10, 5))

    # Balkendiagramm für Arbeitsstunden erstellen
    ax.bar(monthly_days_no_year, work_hours, color='skyblue', label='Arbeitsstunden')

    # Pausenzeiten für alle Tage akkumulieren
    # TODO here goes IF radio1 true then
    total_break_times = [break_time for break_time in break_times.values() if break_time is not None]

    # Balkendiagramm für Pausenzeiten erstellen
    print(radio_plot_choice.get(), type(radio_plot_choice.get()))
    if radio_plot_choice.get() == 1:
        ax.bar(monthly_days_no_year, total_break_times, width=0.3, color='rebeccapurple', label='Pausenzeiten')


    # Arbeitsstunden in Float konvertieren
    work_hours = [float(hours) for hours in work_hours]

    # Durchschnittliche Arbeitsstunden berechnen
    average_work_hours = sum(work_hours) / len(work_hours)

    # Durchschnittslinie hinzufügen
    ax.axhline(y=average_work_hours, color='orange', linestyle='--', label='Durchschnitt')

    # Achsentitel und Diagrammtitel setzen
    ax.set_xlabel('Datum')
    ax.set_ylabel('Gesamtarbeitsstunden')
    ax.set_title(plot_title)

    # X-Achsenbeschriftungen drehen und rechts ausrichten
    plt.xticks(rotation=45, ha='right')

    # Legende hinzufügen und Layout anpassen
    ax.legend()
    plt.tight_layout()


def math_plot():
    # Funktion zum Berechnen der gearbeiteten Stunden, Lesen von Zeilen mit demselben Monat
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    # Leeres Dictionary für zukünftige Daten: Datum: Arbeitszeit
    work_hours_per_day = {}

    # Datum und Arbeitszeit in Listen
    for row in rows[1:]:
        if len(row) == 3:
            date_time_str = row[0]
            work_hours_str = row[2]
            # Versuch, date_time_str in ein datetime-Objekt zu konvertieren
            date_time = dt.strptime(date_time_str, "%d.%m.%Y-%H:%M:%S")

            check_out_date_str = date_time.strftime("%d.%m.%Y")

            # Arbeitszeit = Arbeitszeit_str
            work_hours = float(work_hours_str)

            # Check, ob der Tag im ausgewählten Monat und Jahr liegt
            selected_month_year = dt.strptime(dropdown_month.get(), '%B %Y').strftime('%m.%Y')
            if check_out_date_str.endswith(selected_month_year):
                # Wenn an diesem Tag bereits gearbeitet wurde, addiere die Arbeitsstunden
                if check_out_date_str in work_hours_per_day:
                    work_hours_per_day[check_out_date_str] += work_hours
                else:
                    work_hours_per_day[check_out_date_str] = work_hours

    # Funktionsaufruf break_times
    break_times = calculate_break_times()

    # Listen für die Erstellung des Diagramms vorbereiten (Trennung von Tagen und Arbeitszeit in separate Listen)
    monthly_days = list(work_hours_per_day.keys())
    work_hours = [work_hours_per_day[day] for day in monthly_days]

    # Funktion zum Erstellen des Diagramms aufrufen
    # TODO or maybe here if without breaktimes
    create_plot(work_hours, monthly_days, break_times, f'Arbeitszeiten {dropdown_month.get()}')

    # Diagramm anzeigen
    plt.show()


current_date = get_date()

# Haupt-Tkinter-Fenster erstellen
root = tk.Tk()
style = ttk.Style(root)
root.tk.call('source', 'style/azure.tcl')
# root.tk.call("set_theme", "light")
root.tk.call("set_theme", "dark")
root.title('Zeiterfassung')

# Bildlabel für den Hintergrund in Tkinter
imagepath = 'img/bg.png'  # TODO: Style - Change bg to something else maybe
img = PhotoImage(file=imagepath)
canvas_bg = tk.Canvas(root, width=img.width() * 0.5, height=img.height() * 0.5)
canvas_bg.create_image(0, 0, anchor=tk.NW, image=img)
canvas_bg.grid(row=0, column=0, rowspan=6, columnspan=6, sticky='nsew')
canvas_bg.lower(tk.ALL)

# Frames mit Rahmen erstellen
frame_0_0 = tk.Frame(root, highlightbackground='#007FFF', highlightthickness=2, padx=15, pady=5, borderwidth=15)
frame_1_0 = tk.Frame(root, highlightbackground='#007FFF', highlightthickness=2, padx=15, pady=5, borderwidth=15)
frame_0_1 = tk.Frame(root, highlightbackground='#007FFF', highlightthickness=2, padx=15, pady=5, borderwidth=15)


# Labels für Datum und Zeit
label_hello = ttk.Label(frame_0_0, text='Hallo, Jannis!', anchor="center", justify="center")
label_timetracking = ttk.Label(frame_0_1, text='Zeiterfassung', anchor="center", justify="center")
label_space = ttk.Label(frame_0_0, text='------------------', anchor="center", justify="center")
label_stats = ttk.Label(frame_1_0, text='Statistiken zur Arbeitszeit', anchor='center', justify='center')
label_date = ttk.Label(frame_0_0, text=current_date, anchor='center', justify='center')
label_time = ttk.Label(frame_0_0, anchor='center', justify='center')

# Buttons und Combobox
get_time()
worked_months = get_worked_months()
button_check_in = ttk.Button(frame_0_1, style='Accent.TButton', text='Check-in', command=check_in, compound="center")
if get_status():
    button_check_in.config(text='Check-out')
button_plot = ttk.Button(frame_1_0, style='Accent.TButton', text='Arbeitszeit aufrufen', command=math_plot)
button_user_quit = ttk.Button(text='Quit', style='Accent.TButton', command=user_quit)

dropdown_month = ttk.Combobox(frame_1_0, values=worked_months, state='readonly')
dropdown_month.current(0)

# Radiobuttons
radio_plot_choice = tk.IntVar()
radio1 = ttk.Radiobutton(frame_1_0, text='Mit Pausenzeiten', variable=radio_plot_choice, value=1)
radio2 = ttk.Radiobutton(frame_1_0, text='Ohne Pausenzeiten', variable=radio_plot_choice, value=2)

# Funktion aufrufen, wenn ein Element im Dropdown ausgewählt wird.
dropdown_month.bind("<<ComboboxSelected>>", highlight_clear)

# Grid-Platzierungen
# Frame 0_0
frame_0_0.grid(row=0, column=0, pady=15, padx=15, sticky='nsew')
label_hello.grid(row=0, column=0, sticky='nsew')
label_space.grid(row=1, column=0, sticky='nsew')
label_date.grid(row=2, column=0, sticky='nsew')
label_time.grid(row=3, column=0, sticky='nsew')

# Frame 0_1
frame_0_1.grid(row=0, column=1, pady=15, padx=15, sticky='nsew')
label_timetracking.grid(row=1, column=0, sticky='nsew')
button_check_in.grid(row=2, column=0, sticky='nsew', pady=5)

# Frame 1_0
frame_1_0.grid(row=1, column=0, columnspan=2, pady=0, padx=15, sticky='nsew')
radio1.grid(row=0, column=0, sticky='nsew', ipadx=20)
radio2.grid(row=1, column=0, sticky='nsew')
dropdown_month.grid(row=0, column=1)
button_plot.grid(row=1, column=1, sticky='nsew', pady=5)

button_user_quit.grid(row=5, column=0, columnspan=2, padx=15, pady=15, sticky='nsew')

radio_plot_choice.set(1)

# Konfiguriere die Gewichtung der Spalten
for i in range(6):
    root.columnconfigure(i, weight=1)

# Setze die Fenstergeometrie
root.geometry("440x335+1000+500")
# root.geometry("483x340+1000+500")

# Starte die Tkinter-Event-Schleife
root.mainloop()

# TODO WIP:
# TODO - Schauen ob es schön aussieht: Nur Pausenzeiten option Radiobuttons
# TODO - Tkinter schöner machen - Framebreite, sowie geometrybreite anpassen
# TODO - Sicherstellen, dass ich seaborn benutze für den plot
# TODO - Tkinter Code sortieren
# TODO - Code Cleanup / Reihenfolge der Funktionen um das Programm am Besten vorstellen zu können
# TODO - Testen auf alle möglichen Fehler
# TODO - Alles erklären können
# TODO - Projekt vorstellen: 15 Minuten Zeit

# TODO DONE:
# DONE: Focus entfernen von geklickten Buttons / Temp Fix with same border color
# DONE: Leeren Frame füllen / Checkout Frame vergrößern und aktuelle Arbeitszeit anzeigen?
# DONE: calculate break times
# DONE: Pause als zweiten Balken ins Matplotlib

# DONE: Generate more data for zeiterfassung
# DONE: Fix break_times mismatch, if there is no break on a date, put 0 in the list
