import locale
import tkinter as tk
from tkinter import ttk, PhotoImage
from datetime import datetime as dt
import csv
import seaborn as sns
import matplotlib.pyplot as plt

# Deutsche Lokalisierung für Datumsformatierung
locale.setlocale(locale.LC_TIME, 'de_DE')

# Dateipfad für die Zeiterfassungsdaten
file = 'zeiterfassung.csv'

# Global Style für Matplotlib setzen
sns.set_style('whitegrid')


# ======= Datetime Funktionen =======
def get_date():
    current_dt = dt.now()
    return current_dt.strftime("%d.%m.%Y")


def get_date_time():
    current_dt = dt.now()
    return current_dt


def get_time():
    current_dt = dt.now()
    current_time = current_dt.strftime("%H:%M:%S")
    label_time.config(text=current_time)
    root.after(1000, get_time)
    return current_time


# ======= .csv Funktionen =======
def read_csv_data(file_path):
    try:  # Öffne die CSV-Datei im Lese-Modus
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            # Lese alle vorhandenen Daten in eine Liste
            rows = list(reader)
        return rows
    # Ausnahmebehandlung
    except FileNotFoundError:
        print(f"Dateipfad {file_path} wurde nicht gefunden.")
    except csv.Error as e:
        print(f"Fehler beim Lesen der .csv Datei: {e}")


def get_status():
    # Überprüfung, ob bereits eingecheckt worden ist, gibt einen Bool-Wert zurück
    existing_data = read_csv_data(file)
    # Überprüfe, ob Daten vorhanden sind und ob die letzte Zeile nur ein Element hat
    if existing_data and len(existing_data[-1]) == 1:
        # Der Benutzer hat bereits eingecheckt
        return True
    else:
        # Der Benutzer hat noch nicht eingecheckt
        return False


def get_worked_months():
    """
        Ermittelt eine Liste von Monaten, in denen Arbeit aufgezeichnet wurde,
        basierend auf den vorhandenen CSV-Daten.

        Rückgabewert:
            Liste: Eine sortierte Liste formatierter Monatsnamen und Jahre.
                   Beispiel: ['Dezember 2023', 'November 2023', 'Oktober 2023']
        """
    # Liest vorhandene Daten aus der CSV-Datei
    existing_data = read_csv_data(file)

    # Set zum Speichern eindeutiger Kombinationen von Monat und Jahr
    worked_months_year = set()

    # Iteriert durch vorhandene Daten
    for row in existing_data[:]:
        # Überprüft, ob die Zeile die drei Elemente hat
        if len(row) == 3:
            # Speichern des Datumsstrings
            date_time_str = row[0]
            try:
                # Konvertiert den Datumsstring in ein Datumsobjekt
                date_time = dt.strptime(date_time_str, "%d.%m.%Y-%H:%M:%S")

                # Formatieren von Monat und Jahr und Hinzufügen zum Set
                month_year = date_time.strftime('%m.%Y')
                worked_months_year.add(month_year)
            except ValueError:
                # Rows mit falschem Datumsformat werden übersprungen
                continue
    # Sortiert das Set der Monats-Jahr-Kombinationen und formatiert sie
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


# ======= Matplotlib-Funktionen =======
def math_plot():
    """
        Erstellt ein Diagramm der gearbeiteten Stunden basierend auf den vorhandenen Zeiterfassungsdaten.

        Die Funktion liest die Zeiterfassungsdaten aus der CSV-Datei, extrahiert die gearbeiteten Stunden pro Tag,
        berechnet Pausenzeiten und erstellt ein Diagramm mit Matplotlib. Das Diagramm zeigt die Gesamtarbeitsstunden
        pro Tag für den ausgewählten Monat und ermöglicht die Option, Pausenzeiten im Diagramm darzustellen.
        """
    # Funktion zum Berechnen der gearbeiteten Stunden, Lesen von Zeilen mit demselben Monat
    existing_data = read_csv_data(file)

    # Leeres Dictionary für zukünftige Daten: "Datum: Arbeitszeit"
    work_hours_per_day = {}

    # Datum und Arbeitszeit in Listen
    for row in existing_data[1:]:
        if len(row) == 3:
            date_time_str = row[0]
            work_hours_str = row[2]
            # date_time_str -> datetime -> Tag.Monat.Jahr
            date_time = dt.strptime(date_time_str, "%d.%m.%Y-%H:%M:%S")
            check_out_date_str = date_time.strftime("%d.%m.%Y")

            # Arbeitszeitstring zu float
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
    create_plot(work_hours, monthly_days, break_times, f'Arbeitszeiten {dropdown_month.get()}')

    # Diagramm anzeigen
    plt.show()


def calculate_break_times():
    """
        Berechnet die Pausenzeiten für jeden Tag im ausgewählten Monat und Jahr.

        Returns:
        break_times (dict): Ein Dictionary, das jedem Tag die entsprechende
        Pausenzeit in Stunden zuordnet.
        """
    # Lese vorhandene Daten aus der CSV-Datei
    existing_data = read_csv_data(file)
    prev_date = None
    prev_check_out = None
    break_times = {}

    for row in existing_data[1:]:
        # Überprüfe, ob es sich um abgeschlossene Arbeitszeiten handelt
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
                    timedelta_hours = timedelta.total_seconds() / 3600

                    # Speichern in break_times Dictionary
                    break_times[curr_date] = timedelta_hours
                else:
                    break_times[curr_date] = 0

                # Setzen des aktuellen Datums bevor der Schleifendurchlauf endet
                prev_date = dt.strptime(row[0], "%d.%m.%Y-%H:%M:%S").strftime("%d.%m.%Y")
                prev_check_out = dt.strptime(row[1], "%d.%m.%Y-%H:%M:%S")
    return break_times


def create_plot(work_hours, monthly_days, break_times, plot_title):
    """
        Erstellt ein Balkendiagramm der gearbeiteten Stunden pro Tag mit Matplotlib.

        Parameters:
            work_hours (list): Eine Liste von gearbeiteten Stunden pro Tag.
            monthly_days (list): Eine Liste von Datumsangaben, die den Tagen im Monat entsprechen.
            break_times (dict): Ein Dictionary, das den Pausenzeiten pro Tag zugeordnet ist.
            plot_title (str): Der Titel des Diagramms.
        """
    # Jahr aus Datumsliste entfernen
    monthly_days_no_year = [day[:-4] for day in monthly_days]

    # Figureobjekt und Koordinatensystem erstellen
    fig, ax = plt.subplots(figsize=(10, 5))

    # Balkendiagramm für Arbeitsstunden erstellen
    ax.bar(monthly_days_no_year, work_hours, color='skyblue', label='Arbeitsstunden')

    # Pausenzeiten für alle Tage setzen
    total_break_times = [break_time for break_time in break_times.values() if break_time is not None]

    # Pausenzeiten nur plotten, wenn dementsprechender Radiobutton ausgewählt ist.
    if radio_plot_choice.get() == 1:
        # Balkendiagramm für Pausenzeiten erstellen
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
    # Layout-Anordnung sicherstellen
    plt.tight_layout()


# ======= Tkinter-Funktionen =======
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
    # Beenden der Uhrzeit Funktion
    root.after_cancel(after_id)
    # Tkinter schließen
    root.destroy()


def highlight_clear(_event):
    # Funktion um neu ausgewähltes Dropdown Element als nicht markiert darzustellen
    current = dropdown_month.get()
    dropdown_month.set('')
    dropdown_month.set(current)


# ======= Tkinter Setup =======
# Hauptfenster erstellen
root = tk.Tk()
style = ttk.Style(root)
root.tk.call('source', 'style/azure.tcl')
root.tk.call("set_theme", "dark")
root.title('Zeiterfassung')

# Bildlabel für den Hintergrund in Tkinter
imagepath = 'img/background.png'
img = PhotoImage(file=imagepath)
canvas_bg = tk.Canvas(root, width=img.width() * 0.5, height=img.height() * 0.5)
canvas_bg.create_image(0, 0, anchor=tk.NW, image=img)
canvas_bg.grid(row=0, column=0, rowspan=6, columnspan=6, sticky='nsew')
canvas_bg.lower(tk.ALL)

# Konfiguriere die Gewichtung der Spalten
for i in range(6):
    root.columnconfigure(i, weight=1)

# Tkinter Auflösung
window_width = 380
window_height = 352

# Bildschirmauflösung
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Mitte berechnen
middle_x = (screen_width - window_width) // 2
middle_y = (screen_height - window_height) // 2

# Fenstergeometrie
root.geometry(f"{window_width}x{window_height}+{middle_x}+{middle_y}")

# Tkinter Widgets
# Frame 0_0
frame_0_0 = tk.Frame(root, highlightbackground='#007FFF', highlightthickness=2, padx=15, pady=5, borderwidth=15)
label_hello = ttk.Label(frame_0_0, text='Hallo, Jannis!', anchor="center", justify="center")
label_space = ttk.Label(frame_0_0, text='------------------', anchor="center", justify="center")
current_date = get_date()
label_date = ttk.Label(frame_0_0, text=current_date, anchor='center', justify='center')
label_time = ttk.Label(frame_0_0, anchor='center', justify='center')
# Speichern der After-ID
after_id = get_time()  # Aufruf zum Setzen und Aktualisieren der Uhrzeit

# Frame 0_1
frame_0_1 = tk.Frame(root, highlightbackground='#007FFF', highlightthickness=2, padx=15, pady=5, borderwidth=15)
label_timetracking = ttk.Label(frame_0_1, text='Zeiterfassung', anchor="center", justify="center")
button_check_in = ttk.Button(frame_0_1, style='Accent.TButton', text='Check-in', command=check_in,
                             compound="center")
if get_status():  # Für den Fall, dass bereits eingecheckt wurde
    button_check_in.config(text='Check-out')

# Frame 1_0
frame_1_0 = tk.Frame(root, highlightbackground='#007FFF', highlightthickness=2, padx=15, pady=0, borderwidth=5)
label_stats = ttk.Label(frame_1_0, text='Statistiken zur Arbeitszeit', anchor='center', justify='center')
# Kontrollvariable für Radiobuttons
radio_plot_choice = tk.IntVar()
radio1 = ttk.Radiobutton(frame_1_0, text='Mit Pausenzeiten', variable=radio_plot_choice, value=1)
radio2 = ttk.Radiobutton(frame_1_0, text='Ohne Pausenzeiten', variable=radio_plot_choice, value=2)
# Dropdown Menü
worked_months = get_worked_months()  # Monate auslesen für Dropdown-Feld
dropdown_month = ttk.Combobox(frame_1_0, values=worked_months, state='readonly')
dropdown_month.current(0)
dropdown_month.bind("<<ComboboxSelected>>", highlight_clear)  # Highlight entfernen nach Combobox-Auswahl
button_plot = ttk.Button(frame_1_0, style='Accent.TButton', text='Arbeitszeit aufrufen', command=math_plot)

button_user_quit = ttk.Button(text='Beenden', style='Accent.TButton', command=user_quit)

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
label_stats.grid(row=0, column=0, columnspan=2, ipady=5)
radio1.grid(row=1, column=0, sticky='nsew', ipadx=5)
radio2.grid(row=2, column=0, sticky='nsew', ipadx=5)
radio_plot_choice.set(1)
dropdown_month.grid(row=1, column=1, padx=5, pady=5)
button_plot.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)

# Tkinter ohne Frame
button_user_quit.grid(row=5, column=0, columnspan=2, padx=15, pady=15, sticky='nsew')

# Starte die Tkinter-Event-Schleife
root.mainloop()
