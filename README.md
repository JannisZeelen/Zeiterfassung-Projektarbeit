# Zeiterfassungsprogramm

Dies ist ein einfaches Zeiterfassungsprogramm, das mit Python und Tkinter erstellt wurde. Es ermöglicht Benutzern, ihre Arbeitszeiten zu verfolgen und Arbeitsstatistiken für bestimmte Monate anzuzeigen.

## Funktionen

- **Check-in / Check-out:** Benutzer können sich ein- und auschecken, um ihre Arbeitszeiten zu erfassen.
- **Arbeitszeitberechnung:** Das Programm berechnet automatisch die Arbeitszeit zwischen Check-in und Check-out.
- **Monatsstatistik:** Benutzer können Statistiken über ihre Arbeitszeiten für bestimmte Monate anzeigen.
- **Pausenberechnung:** Das Programm berechnet die Pausenzeit zwischen aufeinanderfolgenden Check-ins und Check-outs.

## Verwendung

1. **Check-in / Check-out:**
   - Klicken Sie auf die Schaltfläche "Check-in", um sich einzuchecken.
   - Klicken Sie erneut auf die Schaltfläche, um sich auszuchecken.

2. **Monatsstatistik:**
   - Wählen Sie den gewünschten Monat im Dropdown-Menü aus.
   - Klicken Sie auf "Arbeitszeit aufrufen", um die Statistik für den ausgewählten Monat anzuzeigen.

3. **Beenden:**
   - Klicken Sie auf die "Quit"-Schaltfläche, um das Programm zu beenden.

## Voraussetzungen

- Python 3.x
- matplotlib~=3.8.0
- sv_ttk
- Die erforderlichen Python-Pakete können mit `pip install -r requirements.txt` installiert werden.
- pip kann mit `conda install pip` installiert werden.

## Lokalisierung

Das Programm verwendet die deutsche Lokalisierung für die Datumsformatierung.

## Datenpersistenz

Die Zeiterfassungsdaten werden in einer CSV-Datei (`zeiterfassung.csv`) gespeichert.

## Lizenz

Dieses Programm ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für weitere Details.

## Autor

- Jannis Zeelen