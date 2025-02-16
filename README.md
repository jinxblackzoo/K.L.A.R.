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

- Mehrere Karteikarten-Datenbanken 
- Einfache und intuitive Benutzeroberfläche
- Intelligentes Lernsystem für die Karteikarten 
   - Lernsystem nach gemeisterten Level
      - Level 1: Neu eingegebene Karteikarten. Priorität: Sehr hoch. Gewichtung: 4
      - Level 2: Karteikarten, die bereits 4 mal im Level 1 richtig beantwortet wurden. Priorität: hoch. Gewichtung: 3
      - Level 3: Karteikarten, die bereits 6 mal im Level 2 richtig beantwortet wurden. Priorität: normal. Gewichtung: 2
      - Level 4: Karteikarten, die bereits 10 mal im Level 3 richtig beantwortet wurden. Priorität: niedrig. Gewichtung: 1
   - Rückstufung nach Level: 
         - Level 1: 1 mal falsch beantwortet > Erhöhung der Abfragefrequenz um den Faktor 2
         - Level 2: 1 mal falsch beantwortet > Rückstufung auf Level 1 
         - Level 3: 2 mal falsch beantwortet > Rückstufung auf Level 2 
         - Level 4: 2 mal falsch beantwortet > Rückstufung auf Level 3
   - Abfragefrequenz:
         - Level 1:  Alle Karteikarten werden mindestens 5 mal nach dem Zufallsprinzip abgefragt. Bei mindestens 4 richtigen Antworten erfolgt die Hochstufung auf Level 2. Abfrage nach dem Zufallsprinzip mit der Gewichtung 4 
         - Level 2:  Alle Karteikarten werden mindestens 10 mal nach dem Zufallsprinzip abgefragt. Bei mindestens 6 richtigen Antworten erfolgt die Hochstufung auf Level 3. Abfrage nach dem Zufallsprinzip mit der Gewichtung 3 
         - Level 3:  Alle Karteikarten werden mindestens 15 mal nach dem Zufallsprinzip abgefragt. Bei mindestens 10 richtigen Antworten erfolgt die Hochstufung auf Level 4. Abfrage nach dem Zufallsprinzip mit der Gewichtung 2 
         - Level 4:  Alle Karteikarten werden mindestens nach dem Zufallsprinzip abgefragt. Bei Richtiger  Antwort bleibt die Karteikarte auf dem Level und wird weiterhin regelmäßig nach der Gewichtung und dem Zufallsprinzip abgefragt. Abfrage nach dem Zufallsprinzip mit der Gewichtung 1
         Die Abfrage soll generell nach dem Zufallsprinzip erfolgen. Lediglich die Häufigkeit der Abfrage wird sich je nach Level und Gewichtung unterscheiden. Also neue Karteikarten und solche mit einem niedrigem Level und somit hoher Gewichtung háufiger. 

- Fortschrittsüberwachung und PDF-Reports
 
 ## Dateispeicherorte
 
 Das Programm speichert Daten an folgenden Orten:

### Persönliche Daten
- `~/.local/share/voll/databases/`: Karteikarten-Sammlungen
- `~/.local/share/voll/exports/`: Exportierte PDF-Dateien und CSV-Listen
- `~/.local/share/voll/reports/`: Lernfortschritte und Statistiken

### Konfigurationsdateien
- `~/.config/voll/settings.ini`: Programmeinstellungen
- `~/.config/voll/databases.json`: Liste der verfügbaren Karteikarten-Sammlungen
- `~/.config/voll/themes/`: Benutzerdefinierte Themes (optional)

Die Datenbanken können einfach gesichert werden, indem der komplette `~/.local/share/voll` Ordner kopiert wird.

## Installation

Die Installation ist ganz einfach und funktioniert auf allen Linux-Systemen:

1. Öffne ein Terminal (meist mit Strg+Alt+T)

2. Lade V.O.L.L. herunter:
   ```bash
   git clone https://github.com/jinxblackzoo/V.O.L.L.
   cd V.O.L.L.
   ```

3. Starte die Installation:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

Das Installationsprogramm erkennt deine Linux-Version automatisch und installiert alle benötigten Programme. Folge einfach den Anweisungen auf dem Bildschirm.

Nach der Installation findest du V.O.L.L. im Startmenü oder kannst es mit dem Befehl `voll` im Terminal starten.

## Update

Um V.O.L.L. zu aktualisieren:

1. Gehe in das V.O.L.L.-Verzeichnis:
   ```bash
   cd V.O.L.L.
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
mkdir -p ~/voll_backup
cp -r ~/.local/share/voll ~/voll_backup/
```

1. Lösche die Programmdateien:
   ```bash
   # Python-Modul entfernen
   rm -rf ~/.local/lib/python*/site-packages/voll*
   
   # Ausführbare Datei entfernen
   rm -f ~/.local/bin/voll
   
   # Desktop-Integration entfernen
   rm -f ~/.local/share/applications/voll.desktop
   rm -f ~/.local/share/icons/hicolor/scalable/apps/voll.svg
   gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/
   ```

2. Optional: Lösche deine persönlichen Daten (ACHTUNG: Dies löscht alle Vokabeln und Einstellungen!):
```bash
   rm -rf ~/.local/share/voll    # Vokabeldatenbank
   rm -rf ~/.config/voll         # Einstellungen
```

3. Optional: Lösche das Backup, wenn du es nicht mehr brauchst:
```bash
rm -rf ~/.config/voll     # Konfiguration
rm -rf ~/.local/share/voll    # Karteikarten-Sammlungen
```

**Hinweis**: Die Systemabhängigkeiten (GTK4, etc.) werden nicht entfernt, da sie möglicherweise von anderen Programmen verwendet werden.

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
   voll
   ```

### Weitere Hilfe
Wenn du weitere Hilfe brauchst:
1. Öffne ein [Issue auf GitHub](https://github.com/jinxblackzoo/V.O.L.L./issues)
2. Beschreibe dein Problem
3. Füge die Fehlermeldung aus dem Terminal hinzu

## Entwicklung

Möchten Sie zum Projekt beitragen? Hier sind die Schritte:

1. Repository klonen
2. Virtuelle Umgebung erstellen:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
3. Änderungen vornehmen
4. Pull Request erstellen
