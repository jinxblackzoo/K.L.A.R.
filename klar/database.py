#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
K.L.A.R. - Karteikarten Lernen Aber Richtig - Ein kinderfreundlicher Karteikarten-Trainer mit GTK4-Oberfläche
Copyright (C) 2025 jinx@blackzoo.de

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
import random
from datetime import timedelta

Base = declarative_base()

class Flashcard(Base):
    __tablename__ = 'flashcards'
    
    id = Column(Integer, primary_key=True)
    database_name = Column(String, nullable=False)  # Name der Datenbank zu der die Karte gehört
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    keywords = Column(String, nullable=False, default="[]")  # JSON-Array als String
    image_path = Column(String, nullable=True)  # Pfad zum Bild, falls vorhanden
    
    # Statistiken
    correct_count = Column(Integer, default=0)  # Gesamtzahl richtiger Antworten
    wrong_count = Column(Integer, default=0)    # Gesamtzahl falscher Antworten
    level = Column(Integer, default=1)          # Aktuelles Level (1-4)
    level_correct_count = Column(Integer, default=0)  # Richtige Antworten im aktuellen Level
    consecutive_wrong = Column(Integer, default=0)    # Aufeinanderfolgende falsche Antworten im Level
    last_practiced = Column(DateTime, nullable=True)
    practice_count = Column(Integer, default=0)      # Übungen im aktuellen Level
    total_practice_count = Column(Integer, default=0) # Gesamtzahl aller Übungen
    priority_factor = Column(Integer, default=1)     # Erhöhungsfaktor für die Abfragefrequenz

    @property
    def keyword_list(self):
        """Gibt die Keywords als Liste zurück"""
        return json.loads(self.keywords)
    
    @keyword_list.setter
    def keyword_list(self, keywords):
        """Speichert die Keywords als JSON-String"""
        if not isinstance(keywords, list):
            raise ValueError("Keywords müssen als Liste übergeben werden")
        if not (2 <= len(keywords) <= 5):
            raise ValueError("Es müssen 2-5 Keywords angegeben werden")
        self.keywords = json.dumps(keywords)
    
    def get_image_path(self):
        """Gibt den absoluten Pfad zum Bild zurück, falls vorhanden"""
        if not self.image_path:
            return None
        
        # Bilder werden im images-Verzeichnis der Datenbank gespeichert
        db_dir = os.path.dirname(os.path.dirname(self.image_path))
        return os.path.join(db_dir, 'images', os.path.basename(self.image_path))

class StudySession(Base):
    """Speichert Informationen über eine Lernsitzung"""
    __tablename__ = 'study_sessions'
    
    id = Column(Integer, primary_key=True)
    database_name = Column(String, nullable=False)  # Name der Datenbank
    date = Column(DateTime, default=datetime.now)
    duration = Column(Float)
    cards_practiced = Column(Integer)
    correct_answers = Column(Integer)

class PracticeAttempt(Base):
    """Speichert einzelne Übungsversuche einer Karteikarte"""
    __tablename__ = 'practice_attempts'
    
    id = Column(Integer, primary_key=True)
    flashcard_id = Column(Integer, nullable=False)  # ID der Karteikarte
    database_name = Column(String, nullable=False)  # Name der Datenbank
    timestamp = Column(DateTime, default=datetime.now)  # Zeitpunkt des Versuchs
    correct = Column(Boolean, nullable=False)  # War die Antwort richtig?
    level = Column(Integer, nullable=False)  # Level zum Zeitpunkt des Versuchs
    duration = Column(Integer, nullable=False, default=0)  # Dauer der Übung in Sekunden

class MUTSession(Base):
    """Speichert Informationen über M.U.T. Lernsessions"""
    __tablename__ = 'mut_sessions'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    total_answers = Column(Integer, nullable=False)
    topic = Column(String)  # Kann None sein, wenn keine spezifische Kategorie gewählt wurde

class DatabaseManager:
    def __init__(self):
        self.config_dir = os.path.join(
            os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
            'klar'
        )
        self.data_dir = os.path.join(
            os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share')),
            'klar'
        )
        
        # Erstelle die Verzeichnisse
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.config_file = os.path.join(self.config_dir, 'databases.json')
        self.load_config()

    def load_config(self):
        """Lädt die Konfiguration oder erstellt eine neue"""
        config_exists = os.path.exists(self.config_file)
        
        if config_exists:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                
                # Überprüfe, ob die aktive Datenbank tatsächlich existiert
                if self.config['active_db']:
                    db_file = self.config['databases'].get(self.config['active_db'])
                    if db_file:
                        db_path = os.path.join(self.data_dir, db_file)
                        if not os.path.exists(db_path):
                            print(f"Warnung: Aktive Datenbank {db_path} nicht gefunden")
                            self.config['active_db'] = None
                            self.save_config()
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")
                config_exists = False
                
        if not config_exists:
            # Erstelle eine neue Konfiguration mit einer Beispiel-Datenbank
            self.config = {
                'databases': {},
                'active_db': None
            }
            
            # Erstelle die Beispiel-Datenbank beim ersten Start
            try:
                name = "Beispiel"
                db_file = "beispiel.db"
                db_path = os.path.join(self.data_dir, db_file)
                
                # Überprüfe, ob die Datenbankdatei bereits existiert
                if os.path.exists(db_path):
                    print(f"Warnung: Datenbank {db_path} existiert bereits")
                    # Füge sie einfach zur Konfiguration hinzu
                else:
                    # Erstelle die physische Datenbank
                    engine = create_engine(f'sqlite:///{db_path}')
                    Base.metadata.create_all(engine)
                    print(f"Neue Beispiel-Datenbank wurde erstellt")
                
                # Aktualisiere die Konfiguration
                self.config['databases'][name] = db_file
                self.config['active_db'] = name
                self.save_config()
                print(f"Beispiel-Datenbank wurde als aktiv gesetzt")
                
            except Exception as e:
                print(f"Fehler beim Erstellen der Beispiel-Datenbank: {e}")
                self.config = {'databases': {}, 'active_db': None}
        
        self.save_config()

    def save_config(self):
        """Speichert die Konfiguration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

    def get_db_path(self, database=None):
        """Gibt den Pfad zur Datenbank zurück"""
        if database is None:
            database = self.config['active_db']
        
        db_file = self.config['databases'].get(database)
        if not db_file:
            raise ValueError(f"Keine Datenbank für {database} gefunden")
            
        return os.path.join(self.data_dir, db_file)

    def get_available_databases(self):
        """Gibt eine Liste aller verfügbaren Datenbanken zurück"""
        return list(self.config['databases'].keys())

    def get_active_database(self):
        """Gibt die aktive Datenbank zurück"""
        return self.config['active_db']

    def set_active_database(self, database):
        """Setzt die aktive Datenbank"""
        if database not in self.config['databases']:
            raise ValueError(f"Datenbank {database} nicht gefunden")
        
        self.config['active_db'] = database
        self.save_config()

    def add_database(self, database, db_file=None):
        """Fügt eine neue Datenbank hinzu"""
        if database in self.config['databases']:
            raise ValueError(f"Datenbank {database} existiert bereits")
            
        if db_file is None:
            db_file = database.lower().replace(' ', '_') + '.db'
            
        self.config['databases'][database] = db_file
        self.save_config()
        
        # Initialisiere die neue Datenbank
        db_path = os.path.join(self.data_dir, db_file)
        engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(engine)

    def remove_database(self, database):
        """Entfernt eine Datenbank"""
        if database not in self.config['databases']:
            raise ValueError(f"Datenbank {database} nicht gefunden")
            
        db_path = self.get_db_path(database)
        
        # Lösche die Datenbankdatei
        if os.path.exists(db_path):
            os.remove(db_path)
            
        # Entferne den Eintrag aus der Konfiguration
        del self.config['databases'][database]
        
        # Wenn die aktive Datenbank gelöscht wurde, wähle eine andere
        if self.config['active_db'] == database and self.config['databases']:
            self.config['active_db'] = next(iter(self.config['databases']))
            
        self.save_config()

    def create_database(self, name, database):
        """
        Erstellt eine neue Datenbank.
        Args:
            name (str): Der Anzeigename der Datenbank (mit Original-Schreibweise)
            database (str): Der interne Name für die Datenbankdatei (lowercase)
        """
        # Überprüfe ob der Name gültig ist
        if not name or not database:
            raise ValueError("Name und Datenbank dürfen nicht leer sein")
        
        # Überprüfe ob die Datenbank bereits existiert
        if name in self.config['databases']:
            raise ValueError(f"Eine Datenbank für {name} existiert bereits")
        
        # Erstelle die Datenbankdatei
        db_file = database.lower().replace(' ', '_') + '.db'
        db_path = os.path.join(self.data_dir, db_file)
        engine = create_engine(f'sqlite:///{db_path}')
        
        # Erstelle die Tabellen
        Base.metadata.create_all(engine)
        
        # Füge die Datenbank zum Manager hinzu
        self.config['databases'][name] = db_file
        
        # Setze die neue Datenbank als aktiv
        self.config['active_db'] = name
        self.save_config()
        
        return True

    def rename_database(self, old_name, new_name):
        """
        Benennt eine Datenbank um.
        Args:
            old_name (str): Der aktuelle Name der Datenbank
            new_name (str): Der neue Name für die Datenbank
        """
        if not old_name or not new_name:
            raise ValueError("Alter und neuer Name dürfen nicht leer sein")

        if new_name in self.config['databases']:
            raise ValueError(f"Eine Datenbank mit dem Namen {new_name} existiert bereits")

        if old_name not in self.config['databases']:
            raise ValueError(f"Die Datenbank {old_name} existiert nicht")

        # Hole den Dateinamen der alten Datenbank
        old_db_file = self.config['databases'][old_name]
        
        # Erstelle den neuen Dateinamen
        new_db_file = new_name.lower().replace(' ', '_') + '.db'
        
        # Pfade zu den Datenbankdateien
        old_path = os.path.join(self.data_dir, old_db_file)
        new_path = os.path.join(self.data_dir, new_db_file)
        
        # Benenne die Datei um
        os.rename(old_path, new_path)
        
        # Aktualisiere die Konfiguration
        self.config['databases'][new_name] = new_db_file
        del self.config['databases'][old_name]
        
        # Wenn die umbenannte Datenbank die aktive war, aktualisiere den Namen
        if self.config['active_db'] == old_name:
            self.config['active_db'] = new_name
            
        self.save_config()
        
    def delete_database(self, name):
        """
        Löscht eine Datenbank.
        Args:
            name (str): Der Name der zu löschenden Datenbank
        """
        if not name:
            raise ValueError("Name darf nicht leer sein")

        if name not in self.config['databases']:
            raise ValueError(f"Die Datenbank {name} existiert nicht")

        # Hole den Dateinamen
        db_file = self.config['databases'][name]
        db_path = os.path.join(self.data_dir, db_file)
        
        # Lösche die Datei
        if os.path.exists(db_path):
            os.remove(db_path)
        
        # Entferne den Eintrag aus der Konfiguration
        del self.config['databases'][name]
        
        # Wenn die gelöschte Datenbank die aktive war, setze active_db zurück
        if self.config['active_db'] == name:
            self.config['active_db'] = None
            
        self.save_config()

# Globale Instanz des DatabaseManager
db_manager = DatabaseManager()

def init_db(database=None):
    """Initialisiert die Datenbank"""
    if database:
        engine = create_engine(f'sqlite:///{database}')
    else:
        engine = create_engine('sqlite:///:memory:')
    
    # Erstelle alle Tabellen neu
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    return engine

def add_flashcard(session, database_name, question, answer, keywords=None, image_path=None):
    """Fügt eine neue Karteikarte hinzu"""
    if keywords is None:
        keywords = []
    
    card = Flashcard(
        database_name=database_name,
        question=question,
        answer=answer,
        keywords=json.dumps(keywords) if keywords else "[]",
        image_path=image_path
    )
    session.add(card)
    session.commit()
    return card

def get_all_flashcards(session, database_name=None):
    """Gibt alle Karteikarten zurück"""
    if database_name:
        return session.query(Flashcard).filter_by(database_name=database_name).all()
    return session.query(Flashcard).all()

def update_flashcard_stats(session, card_id, correct, database_name, practice_duration=0):
    """
    Aktualisiert die Statistiken einer Karteikarte nach einer Antwort.
    
    Level-System:
    - Level 1: Neue Karten, Gewichtung 4
      - Min. 5 Übungen, 4 richtig für Aufstieg
      - Bei Fehler: Frequenz × 2
    - Level 2: Fortgeschritten, Gewichtung 3
      - Min. 10 Übungen, 6 richtig für Aufstieg
      - Bei 1 Fehler: Zurück zu Level 1
    - Level 3: Gefestigt, Gewichtung 2
      - Min. 15 Übungen, 10 richtig für Aufstieg
      - Bei 2 Fehlern: Zurück zu Level 2
    - Level 4: Gemeistert, Gewichtung 1
      - Regelmäßige Wiederholung
      - Bei 2 Fehlern: Zurück zu Level 3
    
    Args:
        session: SQLAlchemy Session
        card_id: ID der Karteikarte
        correct: True wenn Antwort richtig, False sonst
        database_name: Name der Datenbank
        practice_duration: Dauer der Übung in Sekunden
    """
    # Hole die Karteikarte und prüfe ob sie zur richtigen Datenbank gehört
    card = session.query(Flashcard).filter(
        Flashcard.id == card_id,
        Flashcard.database_name == database_name  # Wichtig: Prüfe Datenbankzugehörigkeit
    ).first()
    
    if not card:
        return
        
    # Erstelle einen neuen Übungsversuch mit Zeitstempel
    attempt = PracticeAttempt(
        flashcard_id=card_id,
        database_name=database_name,
        correct=correct,
        level=card.level,
        duration=practice_duration  # Speichere die Übungsdauer
    )
    session.add(attempt)
    
    # Aktualisiere die Kartenstatistiken
    card.practice_count += 1      # Übungen im aktuellen Level
    card.total_practice_count += 1 # Gesamte Übungen (wird nie zurückgesetzt)
    
    if correct:
        card.correct_count += 1
        card.level_correct_count += 1  # Richtige Antworten im Level
        card.consecutive_wrong = 0     # Fehlersträhne zurücksetzen
        
        # Prüfe Level-Aufstieg gemäß README.md
        if card.level == 1 and card.level_correct_count >= 4 and card.practice_count >= 5:
            card.level = 2  # Aufstieg zu Level 2 (Gewichtung 3)
            card.level_correct_count = 0
            card.practice_count = 0
            card.priority_factor = 1
        elif card.level == 2 and card.level_correct_count >= 6 and card.practice_count >= 10:
            card.level = 3  # Aufstieg zu Level 3 (Gewichtung 2)
            card.level_correct_count = 0
            card.practice_count = 0
            card.priority_factor = 1
        elif card.level == 3 and card.level_correct_count >= 10 and card.practice_count >= 15:
            card.level = 4  # Aufstieg zu Level 4 (Gewichtung 1)
            card.level_correct_count = 0
            card.practice_count = 0
            card.priority_factor = 1
    else:
        card.wrong_count += 1
        card.consecutive_wrong += 1     # Fehlersträhne erhöhen
        
        # Rückstufung und Frequenzerhöhung gemäß README.md
        if card.level == 1:
            card.priority_factor *= 2  # Level 1: Erhöhung der Abfragefrequenz
        elif card.level == 2 and card.consecutive_wrong >= 1:
            card.level = 1  # Nach 1 Fehler zurück zu Level 1
            card.level_correct_count = 0
            card.practice_count = 0
            card.priority_factor = 1
        elif card.level == 3 and card.consecutive_wrong >= 2:
            card.level = 2  # Nach 2 Fehlern zurück zu Level 2
            card.level_correct_count = 0
            card.practice_count = 0
            card.priority_factor = 1
        elif card.level == 4 and card.consecutive_wrong >= 2:
            card.level = 3  # Nach 2 Fehlern zurück zu Level 3
            card.level_correct_count = 0
            card.practice_count = 0
            card.priority_factor = 1
        
    card.last_practiced = datetime.now()
    session.commit()

def get_card_for_practice(session, database_name=None):
    """
    Wählt eine Karteikarte zum Üben aus basierend auf Level und Gewichtung.
    
    Bemerkungen:
    - Karten werden nach dem Zufallsprinzip ausgewählt
    - Die Auswahlwahrscheinlichkeit wird durch Level bestimmt:
      Level 1: Gewichtung 4 (neue Karten, häufiger üben)
      Level 2: Gewichtung 3
      Level 3: Gewichtung 2
      Level 4: Gewichtung 1 (gemeisterte Karten, seltener üben)
    """
    query = session.query(Flashcard)
    if database_name:
        query = query.filter_by(database_name=database_name)
    
    # Hole alle Karten
    cards = query.all()
    if not cards:
        return None

    # Erstelle gewichtete Liste basierend auf Level
    weighted_cards = []
    for card in cards:
        # Basisgewichtung nach Level (4,3,2,1)
        weight = 5 - card.level
        # Füge Karte entsprechend oft zur Liste hinzu
        weighted_cards.extend([card] * weight)
    
    # Wähle zufällig eine Karte aus der gewichteten Liste
    if weighted_cards:
        return random.choice(weighted_cards)
        
    # Fallback: Komplett zufällige Auswahl wenn keine Gewichtungen
    return random.choice(cards)

def get_flashcard_stats(session):
    """Gibt Statistiken über den Lernfortschritt zurück"""
    total = session.query(Flashcard).count()
    mastered = session.query(Flashcard).filter(Flashcard.level == 4).count()
    in_progress = total - mastered
    
    return {
        'total': total,
        'mastered': mastered,
        'in_progress': in_progress,
        'mastery_rate': (mastered / total * 100) if total > 0 else 0
    }

def add_study_session(session, database_name, duration, cards_practiced, correct_answers):
    """Fügt eine neue Lernsitzung hinzu"""
    study_session = StudySession(
        database_name=database_name,
        duration=duration,
        cards_practiced=cards_practiced,
        correct_answers=correct_answers
    )
    session.add(study_session)
    session.commit()

def get_weekly_stats(session):
    """Hole die Statistiken der letzten 7 Tage"""
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    return session.query(StudySession).filter(StudySession.date >= week_ago).all()

def get_database_stats(session, database=None):
    """Hole Statistiken für eine bestimmte Datenbank oder alle Datenbanken"""
    stats = {}
    
    # Bestimme die zu verarbeitenden Datenbanken
    if database:
        databases = [database]
    else:
        databases = db_manager.get_available_databases()
    
    # Für jede Datenbank
    for db in databases:
        # Hole alle Karten der Datenbank
        cards = session.query(Flashcard).filter(
            Flashcard.database_name == db
        ).all()
        
        # Aktuelle Zeit für Zeitberechnungen
        now = datetime.now()
        
        # Zähle Karten pro Level und berechne Level-Statistiken
        cards_per_level = {1: 0, 2: 0, 3: 0, 4: 0}
        success_rate_per_level = {1: 0, 2: 0, 3: 0, 4: 0}  # Erfolgsquote pro Level
        total_attempts_per_level = {1: 0, 2: 0, 3: 0, 4: 0}  # Versuche pro Level
        
        # Zeiträume für die Statistiken
        time_ranges = {
            'last_7_days': now - timedelta(days=7),
            'last_30_days': now - timedelta(days=30),
            'last_365_days': now - timedelta(days=365)
        }
        
        # Statistiken für verschiedene Zeiträume
        practice_stats = {
            'last_7_days': {'attempts': 0, 'correct': 0, 'duration': 0},
            'last_30_days': {'attempts': 0, 'correct': 0, 'duration': 0},
            'last_365_days': {'attempts': 0, 'correct': 0, 'duration': 0},
            'all_time': {'attempts': 0, 'correct': 0, 'duration': 0}
        }
        
        # Hole alle Übungsversuche für diese Datenbank
        attempts = session.query(PracticeAttempt).filter(
            PracticeAttempt.database_name == db
        ).all()
        
        # Verarbeite jeden Übungsversuch
        for attempt in attempts:
            # Zähle für Gesamtstatistik
            practice_stats['all_time']['attempts'] += 1
            practice_stats['all_time']['duration'] += attempt.duration
            if attempt.correct:
                practice_stats['all_time']['correct'] += 1
            
            # Prüfe für jeden Zeitraum
            for range_name, start_date in time_ranges.items():
                if attempt.timestamp >= start_date:
                    practice_stats[range_name]['attempts'] += 1
                    practice_stats[range_name]['duration'] += attempt.duration
                    if attempt.correct:
                        practice_stats[range_name]['correct'] += 1
        
        # Berechne durchschnittliche Übungszeiten und Erfolgsquoten
        for range_name in practice_stats:
            stats_range = practice_stats[range_name]
            if stats_range['attempts'] > 0:
                stats_range['avg_duration'] = stats_range['duration'] / stats_range['attempts']
                stats_range['success_rate'] = (stats_range['correct'] / stats_range['attempts']) * 100
            else:
                stats_range['avg_duration'] = 0
                stats_range['success_rate'] = 0
        
        # Speichere die Statistiken
        stats[db] = {
            'cards_per_level': cards_per_level,
            'total_cards': len(cards),
            'practice_stats': practice_stats
        }
    
    return stats

def get_mut_stats(session, time_range=None):
    """
    Holt die M.U.T. Statistiken aus der Datenbank.
    
    Args:
        session: SQLAlchemy Session
        time_range (str, optional): Zeitbereich für die Statistiken ('week', 'month', 'year')
    
    Returns:
        dict: Dictionary mit den Statistiken
    """
    query = session.query(MUTSession)
    
    if time_range:
        if time_range == 'week':
            start_date = datetime.now() - timedelta(days=7)
        elif time_range == 'month':
            start_date = datetime.now() - timedelta(days=30)
        elif time_range == 'year':
            start_date = datetime.now() - timedelta(days=365)
        query = query.filter(MUTSession.start_time >= start_date)
    
    sessions = query.all()
    
    if not sessions:
        return {
            'total_sessions': 0,
            'total_duration': 0,
            'total_answers': 0,
            'correct_answers': 0,
            'success_rate': 0,
            'sessions': []
        }
    
    total_duration = sum(session.duration_seconds for session in sessions)
    total_answers = sum(session.total_answers for session in sessions)
    correct_answers = sum(session.correct_answers for session in sessions)
    success_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0
    
    return {
        'total_sessions': len(sessions),
        'total_duration': total_duration,
        'total_answers': total_answers,
        'correct_answers': correct_answers,
        'success_rate': success_rate,
        'sessions': [{
            'start_time': session.start_time.strftime("%d.%m.%Y %H:%M"),
            'end_time': session.end_time.strftime("%d.%m.%Y %H:%M"),
            'duration': session.duration_seconds,
            'correct': session.correct_answers,
            'total': session.total_answers,
            'topic': session.topic
        } for session in sessions]
    }

def format_duration(seconds):
    """
    Formatiert Sekunden in HH:MM:SS Format.
    Die Stunden laufen unbegrenzt weiter (kein Reset bei 99).
    
    Args:
        seconds (float): Zeit in Sekunden
        
    Returns:
        str: Formatierte Zeit im Format HH:MM:SS
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    # Für Stunden unter 100 verwenden wir 2 Stellen, darüber die nötige Anzahl
    if hours < 100:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours}:{minutes:02d}:{seconds:02d}"

def export_flashcards_to_csv(session, filepath):
    """Exportiert die Karteikarten in eine CSV-Datei"""
    cards = session.query(Flashcard).all()
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        # Header
        writer.writerow(['Frage', 'Antwort', 'Richtige', 'Falsche', 'Level', 'Keywords'])
        # Daten
        for card in cards:
            writer.writerow([card.question, card.answer, card.correct_count, card.wrong_count, card.level, ', '.join(card.keyword_list)])

def update_database_structure(database=None):
    """
    Aktualisiert die Datenbankstruktur ohne Datenverlust.
    Führt notwendige Migrationen für Schema-Änderungen durch.
    
    Args:
        database: Optional, Name der zu aktualisierenden Datenbank
    """
    if database:
        engine = create_engine(f'sqlite:///{db_manager.get_db_path(database)}')
    else:
        engine = create_engine('sqlite:///:memory:')
    
    # Verbindung für direkte SQL-Befehle
    connection = engine.connect()
    
    try:
        # 1. Prüfe ob duration Spalte existiert
        has_duration = False
        result = connection.execute(text("PRAGMA table_info(practice_attempts)"))
        for row in result:
            if row[1] == 'duration':  # row[1] ist der Spaltenname
                has_duration = True
                break
        
        # 2. Füge duration Spalte hinzu wenn sie fehlt
        if not has_duration:
            connection.execute(
                text("ALTER TABLE practice_attempts ADD COLUMN duration INTEGER NOT NULL DEFAULT 0")
            )
            
        # Hier können weitere Migrationen hinzugefügt werden
        
        connection.commit()
    except Exception as e:
        print(f"Fehler bei der Datenbankaktualisierung: {str(e)}")
        connection.rollback()
        raise
    finally:
        connection.close()
