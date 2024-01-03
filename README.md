**Zeiterfassungs-App**

## Beschreibung
Die Zeiterfassungs-App ist eine einfache Anwendung, die es Benutzern ermöglicht, ihre Arbeitszeiten zu verfolgen und statistische Analysen über ihre Arbeitszeiten durchzuführen. Die App wurde mit Python und dem Tkinter-Framework für die Benutzeroberfläche entwickelt.

## Funktionen
1. **Check-in und Check-out:**
   - Die Benutzer können sich durch Klicken auf den "Check-in" oder "Check-out" Button ein- bzw. auschecken.
   - Die App speichert die Check-in- und Check-out-Zeiten in einer CSV-Datei.

2. **Arbeitszeitstatistiken:**
   - Die App bietet statistische Analysen über die gearbeiteten Stunden anhand von Diagrammen.
   - Benutzer können wählen, ob Pausenzeiten in den Diagrammen berücksichtigt werden sollen.

3. **Monatsauswahl:**
   - Benutzer können den gewünschten Monat aus einer Dropdown-Liste auswählen.
   - Die App zeigt dann Arbeitszeitstatistiken für den ausgewählten Monat an.

## Dateistruktur
- **zeiterfassung.py:** Hauptprogramm, das die Benutzeroberfläche und die Kernfunktionalitäten enthält.
- **zeiterfassung.csv:** CSV-Datei zur Speicherung von Check-in- und Check-out-Zeiten.

## Abhängigkeiten
Die App verwendet die folgenden Python-Bibliotheken:
- `tkinter`: Für die Erstellung der Benutzeroberfläche.
- `csv`: Zum Lesen und Schreiben von CSV-Dateien.
- `seaborn` und `matplotlib`: Für die Erstellung von Diagrammen.

## Anwendung
1. Führen Sie das Hauptprogramm `zeiterfassung.py` aus.
2. Klicken Sie auf den "Check-in" Button, um sich einzuchecken, oder auf den "Check-out" Button, um sich auszuchecken.
3. Wählen Sie einen Monat aus der Dropdown-Liste aus.
4. Klicken Sie auf den "Arbeitszeit aufrufen" Button, um die Statistiken anzuzeigen.
5. Um das Programm zu beenden klicken Sie auf den "Schließen" Button.
## Lizenz
Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).

Viel Spaß beim Verwenden der Zeiterfassungs-App!