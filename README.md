# K.L.A.R. - Karteikarten Lernen Aber Richtig

Ein kinderfreundlicher Karteikarten-Trainer mit moderner GTK4-Oberfläche, der das Lernen von Karteikarten spannend und unterhaltsam macht. Zusätzlich gibt er Lehrern, Erzeihungsberechtigten und Lernenden ein System zur Kontrolle und Selbstkontrolle mittels eines Reportingsystems.

## Autor
jinx@blackzoo.de

## Entwicklung
Dieses Projekt wurde mit Unterstützung von Künstlicher Intelligenz (Codeium Cascade) entwickelt.

## Lizenz
Dieses Projekt steht unter der [GNU General Public License v3 (GPLv3)](LICENSE).
Copyright (C) 2025 jinx@blackzoo.de

## Features

### Karteikarten-Management
- Mehrere Karteikarten-Datenbanken parallel verwalten
- Einfache und intuitive Benutzeroberfläche
- Import und Export von Karteikarten

### Intelligentes Lernsystem
- **Lernsystem nach gemeisterten Level**
   - Level 1: Neu eingegebene Karteikarten. Priorität: Sehr hoch. Gewichtung: 4
   - Level 2: Karteikarten, die bereits 4 mal im Level 1 richtig beantwortet wurden. Priorität: hoch. Gewichtung: 3
   - Level 3: Karteikarten, die bereits 6 mal im Level 2 richtig beantwortet wurden. Priorität: normal. Gewichtung: 2
   - Level 4: Karteikarten, die bereits 10 mal im Level 3 richtig beantwortet wurden. Priorität: niedrig. Gewichtung: 1

- **Rückstufungssystem** 
   - Level 1: 1 mal falsch beantwortet > Erhöhung der Abfragefrequenz um den Faktor 2
   - Level 2: 1 mal falsch beantwortet > Rückstufung auf Level 1 
   - Level 3: 2 mal falsch beantwortet > Rückstufung auf Level 2 
   - Level 4: 2 mal falsch beantwortet > Rückstufung auf Level 3

- **Intelligente Abfragefrequenz**
   - Level 1: Mindestens 5 Abfragen, 4 richtige für Aufstieg, Gewichtung 4
   - Level 2: Mindestens 10 Abfragen, 6 richtige für Aufstieg, Gewichtung 3
   - Level 3: Mindestens 15 Abfragen, 10 richtige für Aufstieg, Gewichtung 2
   - Level 4: Regelmäßige Wiederholung, Gewichtung 1

### M.U.T. - Maßeinheiten Training
- **Interaktives Übungssystem für Maßeinheiten-Umrechnung**
  - Unterstützt alle gängigen SI-Einheiten
  - Dynamische Aufgabengenerierung
  - Intelligente Rundung und Toleranzberechnung
  - Unterstützung für Komma- und Punktnotation

- **Kategoriebasiertes Training**
  - Längeneinheiten (m, km, cm, mm, etc.)
  - Flächeneinheiten (m², km², cm², etc.)
  - Volumeneinheiten (m³, l, ml, etc.)
  - Gewichtseinheiten (kg, g, mg, etc.)
  - Zeiteinheiten (s, min, h, etc.)
  - Temperatureinheiten (°C, K, °F)

### Umfassendes Reporting-System
- **Zeitbasierte Auswertung**
  - Erfassung aller Lernaktivitäten mit Zeitstempeln
  - Auswertung über verschiedene Zeiträume:
    - Letzte 7 Tage
    - Letzte 30 Tage
    - Letztes Jahr
    - Gesamtzeitraum

- **Detaillierte Statistiken**
  - Karteikarten-Statistiken
    - Lernfortschritt pro Level
    - Erfolgsquoten und Rückstufungen
    - Durchschnittliche Übungszeiten pro Karte
  - M.U.T.-Statistiken
    - Anzahl der Trainingssessions
    - Gesamtdauer des Trainings
    - Erfolgsquoten pro Kategorie
    - Themenspezifische Auswertung

- **Übersichtliche Darstellung**
  - Separate Tabs für verschiedene Bereiche
  - Filterung nach Zeiträumen und Kategorien
  - Export-Möglichkeiten für Reports

## Dateispeicherorte
 
Das Programm speichert Daten an folgenden Orten:

> **Hinweis für Linux-Einsteiger**: 
> Die Tilde (`~`) steht für dein persönliches Benutzerverzeichnis. Unter Linux ist dies meist `/home/deinbenutzername`. 
> Zum Beispiel: Wenn dein Benutzername "lisa" ist, dann ist `~/.local` der Ordner `/home/lisa/.local`.
> Ordner, die mit einem Punkt beginnen (z.B. `.local` oder `.config`), sind versteckte Ordner. Du kannst sie im Dateimanager mit der Tastenkombination `Strg+H` sichtbar machen.

### Persönliche Daten
- `~/.local/share/klar/databases/`: Karteikarten-Sammlungen und M.U.T.-Statistiken
- `~/.local/share/klar/exports/`: Exportierte PDF-Dateien, CSV-Listen und Statistik-Reports
- `~/.local/share/klar/reports/`: Lernfortschritte und detaillierte Auswertungen
  - `cards/`: Karteikarten-Statistiken
  - `mut/`: M.U.T.-Trainingsauswertungen

### Konfigurationsdateien
- `~/.config/klar/settings.ini`: Programmeinstellungen
- `~/.config/klar/databases.json`: Liste der verfügbaren Karteikarten-Sammlungen
- `~/.config/klar/mut_config.json`: M.U.T.-Konfiguration und Einheitenpräferenzen
- `~/.config/klar/themes/`: Benutzerdefinierte Themes (optional)

Die Datenbanken können einfach gesichert werden, indem der komplette `~/.local/share/klar` Ordner kopiert wird.

### Backup und Wiederherstellung

#### Backup erstellen
```bash
# Backup-Verzeichnis erstellen (falls nicht vorhanden)
mkdir -p ~/klar_backup

# Aktuelles Datum zum Backup-Namen hinzufügen
backup_date=$(date +%Y-%m-%d)
backup_dir="$HOME/klar_backup/klar_$backup_date"

# Backup aller Daten erstellen
mkdir -p "$backup_dir"
cp -r ~/.local/share/klar/* "$backup_dir/"
cp -r ~/.config/klar/* "$backup_dir/config/"

# Optional: Backup komprimieren
cd ~/klar_backup
tar czf "klar_backup_$backup_date.tar.gz" "klar_$backup_date"
```

#### Backup wiederherstellen
```bash
# WICHTIG: Stelle sicher, dass K.L.A.R. nicht läuft!

# 1. Backup entpacken (falls komprimiert)
cd ~/klar_backup
tar xzf klar_backup_DATUM.tar.gz   # Ersetze DATUM mit dem Backup-Datum

# 2. Stelle sicher, dass die Zielverzeichnisse existieren
mkdir -p ~/.local/share/klar
mkdir -p ~/.config/klar

# 3. Daten wiederherstellen
cp -r ~/klar_backup/klar_DATUM/* ~/.local/share/klar/
cp -r ~/klar_backup/klar_DATUM/config/* ~/.config/klar/

# 4. Berechtigungen korrigieren
chmod -R u+rw ~/.local/share/klar
chmod -R u+rw ~/.config/klar
```

> **Tipp**: Erstelle regelmäßige Backups deiner Daten, besonders vor Updates oder größeren Änderungen. Die Backup-Dateien kannst du auch auf einem USB-Stick oder in deiner Cloud speichern.

## Installation

Die Installation ist ganz einfach und funktioniert auf allen Linux-Systemen:

1. Öffne ein Terminal (meist mit Strg+Alt+T)

2. Lade K.L.A.R. herunter:
   ```bash
   git clone https://github.com/jinxblackzoo/K.L.A.R.
   cd K.L.A.R.
   ```

3. Starte die Installation:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

Das Installationsprogramm erkennt deine Linux-Version automatisch und installiert alle benötigten Programme. Folge einfach den Anweisungen auf dem Bildschirm.

Nach der Installation findest du K.L.A.R. im Startmenü oder kannst es mit dem Befehl `klar` im Terminal starten.

## Update

Um K.L.A.R. zu aktualisieren:

1. Gehe in das K.L.A.R.-Verzeichnis:
   ```bash
   cd K.L.A.R.
   ```

2. Hole die neueste Version:
   ```bash
   git pull
   ```

3. Installiere das Update:
   ```bash
   ./install.sh
   ```

## Deinstallation

**WICHTIG**: Erstelle vor der Deinstallation ein Backup deiner Karteikarten-Sammlungen, wenn du sie später noch brauchst:
```bash
# Backup erstellen
mkdir -p ~/klar_backup
cp -r ~/.local/share/klar ~/klar_backup/
```

1. Lösche die Programmdateien:
   ```bash
   # Python-Modul entfernen
   rm -rf ~/.local/lib/python*/site-packages/klar*
   
   # Konfigurationsdateien entfernen
   rm -rf ~/.config/klar
   
   # Programmdaten entfernen (ACHTUNG: Löscht alle Karteikarten!)
   rm -rf ~/.local/share/klar
   
   # Desktop-Verknüpfung entfernen
   rm ~/.local/share/applications/klar.desktop
   ```

2. Optional: Entferne das Quellverzeichnis:
   ```bash
   rm -rf ~/K.L.A.R.
   ```

## Probleme?

### Programm startet nicht
1. **Fehlende Abhängigkeiten**: 
   Starte das Installationsskript erneut:
   ```bash
   ./install.sh
   ```

2. **Programm nicht im PATH**:
   - Öffne ein neues Terminal oder starte deinen Computer neu
   - Oder füge diese Zeile in deine `~/.bashrc` ein:
     ```bash
     export PATH="$HOME/.local/bin:$PATH"
     ```

3. **Fehlermeldungen anzeigen**:
   Starte das Programm im Terminal:
   ```bash
   klar
   ```

### Weitere Hilfe
Wenn du weitere Hilfe brauchst:
1. Öffne ein [Issue auf GitHub](https://github.com/jinxblackzoo/K.L.A.R./issues)
2. Beschreibe dein Problem
3. Füge die Fehlermeldung aus dem Terminal hinzu

## Entwicklung

Möchten Sie zum Projekt beitragen? Hier sind die Schritte:

1. Repository klonen:
   ```bash
   git clone https://github.com/jinxblackzoo/K.L.A.R.
   cd K.L.A.R.
   ```

2. Virtuelle Umgebung erstellen:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

3. Abhängigkeiten installieren:
   ```bash
   # Für Debian/Ubuntu
   sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-4.0

   # Für Fedora
   sudo dnf install python3-gobject gtk4
   
   # Für Arch Linux
   sudo pacman -S python-gobject gtk4
   ```

4. Änderungen vornehmen und testen

5. Pull Request erstellen:
   - Fork das Repository auf GitHub
   - Erstelle einen neuen Branch für deine Änderungen
   - Committe deine Änderungen
   - Erstelle einen Pull Request
