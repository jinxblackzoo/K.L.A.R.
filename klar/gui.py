# 1. Einführung

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


# 2. Importe und Abhängigkeiten

import os
import gi
import json
from datetime import datetime, timedelta

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gdk, Gio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from klar.database import (
    init_db, add_flashcard, get_all_flashcards, update_flashcard_stats,
    db_manager, get_card_for_practice, get_flashcard_stats, get_database_stats,
    add_study_session, Base, update_database_structure  # update_database_structure hier importieren
)
import subprocess
import random


# 3. Hauptfenster

class MainWindow(Gtk.ApplicationWindow):
    """
    Hauptfenster der Anwendung.
    """

    def __init__(self, **kwargs):
        """
        Initialisiert das Hauptfenster der Anwendung.
        """
        super().__init__(**kwargs)
        self.set_title("K.L.A.R. - Lerne mit Karteikarten!")
        self.set_default_size(800, 600)

        # Datenbank initialisieren
        self.update_database_connection()

        # Hauptbox
        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=20,
            margin_top=30,
            margin_bottom=30,
            margin_start=30,
            margin_end=30
        )
        self.set_child(self.main_box)

        # Content Stack für verschiedene Ansichten
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_box.append(self.content_stack)

        # Zurück-Button (anfangs versteckt)
        self.back_button = Gtk.Button(label="Zurück zum Hauptmenü")
        self.back_button.connect("clicked", self.show_main_menu)
        self.back_button.set_visible(False)
        self.back_button.set_margin_bottom(20)
        self.main_box.prepend(self.back_button)

        # Hauptmenü erstellen
        self.create_main_menu()

    def create_main_menu(self):
        """
        Erstellt das Hauptmenü mit der aktualisierten Struktur.
        """
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Hauptmenü Container
        menu_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=20,
            margin_top=30,
            margin_bottom=30
        )
        menu_box.set_halign(Gtk.Align.CENTER)
        menu_box.set_valign(Gtk.Align.CENTER)

        # Willkommens-Label
        welcome_label = Gtk.Label()
        welcome_label.set_markup(
            "<span size='xx-large' weight='bold'>Willkommen bei K.L.A.R.!</span>\n"
            "<span size='large'>Karteikarten Lernen Aber Richtig</span>"
        )
        menu_box.append(welcome_label)

        # A. Neue Karteikartesammlung erstellen
        new_collection_button = Gtk.Button(label="Neue Karteikarten-Sammlung erstellen")
        new_collection_button.set_margin_top(20)
        new_collection_button.connect("clicked", self.show_new_database_dialog)
        menu_box.append(new_collection_button)

        # B. Meine Karteikartesammlungen
        collections_button = Gtk.Button(label="Meine Karteikarten-Sammlungen")
        collections_button.connect("clicked", self.show_databases_menu)
        menu_box.append(collections_button)

        # C. Reports
        reports_button = Gtk.Button(label="Reports")
        reports_button.connect("clicked", self.show_reports)
        menu_box.append(reports_button)

        self.content_stack.add_named(menu_box, "menu")
        self.content_stack.set_visible_child_name("menu")

    def show_main_menu(self, button=None):
        """
        Zeigt das Hauptmenü an.
        - Leert den Content Stack und erstellt das Hauptmenü neu.
        - Versteckt den Zurück-Button.
        """
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Hauptmenü neu erstellen
        self.create_main_menu()
        self.back_button.set_visible(False)

    def show_database_content(self, database):
        """
        Zeigt den Inhalt einer ausgewählten Datenbank an.
        - Versteckt das Hauptmenü und leert den Content Stack.
        - Erstellt eine Ansicht mit Aktionsbuttons zum Hinzufügen, Üben und Bearbeiten von Karteikarten.
        """
        # Hauptmenü verstecken
        self.back_button.set_visible(True)

        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Datenbank-Inhalt erstellen
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>{database}</span>")
        content_box.append(title_label)

        # Aktionsbuttons
        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=20,
            margin_top=20
        )
        button_box.set_halign(Gtk.Align.CENTER)

        add_button = Gtk.Button(label="Karteikarten hinzufügen")
        add_button.connect("clicked", self.show_add_dialog)
        button_box.append(add_button)

        practice_button = Gtk.Button(label="Karteikarten üben")
        practice_button.connect("clicked", self.show_practice_dialog)
        button_box.append(practice_button)

        edit_button = Gtk.Button(label="Datenbank bearbeiten")
        edit_button.connect("clicked", self.edit_database)
        button_box.append(edit_button)

        content_box.append(button_box)

        self.content_stack.add_named(content_box, "database")
        self.content_stack.set_visible_child_name("database")

    def edit_database(self, button, database_name):
        """
        Öffnet ein Fenster zum Bearbeiten der Karteikarten.
        - Leert den Content Stack und erstellt eine Bearbeitungsansicht.
        - Fügt eine scrollbare Liste mit den Karteikarten hinzu.
        """
        if not database_name:
            return

        # Aktualisiere die Datenbankverbindung
        self.update_database_connection(database_name)

        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Bearbeitungs-Box erstellen
        edit_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>Karteikarten bearbeiten - {database_name}</span>")
        edit_box.append(title_label)

        # Zurück-Pfeil
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", lambda b: self.show_collection_menu(database_name))
        back_button.set_halign(Gtk.Align.START)
        edit_box.append(back_button)

        # Scrollbare Liste erstellen
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)

        # Liste für Karteikarten
        list_box = Gtk.ListBox()
        list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        scroll.set_child(list_box)

        # Karteikarten laden und anzeigen
        cards = get_all_flashcards(self.session, database_name)
        for card in cards:
            # Box für Karteikarte
            card_box = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=10,
                margin_top=5,
                margin_bottom=5,
                margin_start=10,
                margin_end=10
            )

            # Frage-Eingabefeld
            question_entry = Gtk.Entry()
            question_entry.set_text(card.question)
            question_entry.set_hexpand(True)
            question_entry.connect('activate', self.on_card_changed, card, 'question')
            card_box.append(question_entry)

            # Antwort-Eingabefeld
            answer_entry = Gtk.Entry()
            answer_entry.set_text(card.answer)
            answer_entry.set_hexpand(True)
            answer_entry.connect('activate', self.on_card_changed, card, 'answer')
            card_box.append(answer_entry)

            # Statistik-Label
            stats_label = Gtk.Label()
            stats_label.set_markup(
                f"<span size='small'>✓ {card.correct_count} | ✗ {card.wrong_count}</span>"
            )
            stats_label.set_margin_start(10)
            stats_label.set_margin_end(10)
            card_box.append(stats_label)

            # Löschen-Button
            delete_button = Gtk.Button()
            delete_button.set_icon_name("user-trash-symbolic")
            delete_button.connect('clicked', self.on_card_delete, card, list_box, card_box)
            card_box.append(delete_button)

            # Zur Liste hinzufügen
            list_box.append(card_box)

        edit_box.append(scroll)

        # Button-Box
        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
            margin_top=10
        )
        button_box.set_halign(Gtk.Align.CENTER)

        cancel_button = Gtk.Button(label="Abbrechen")
        cancel_button.connect('clicked', lambda b: self.show_main_menu(b))
        button_box.append(cancel_button)

        save_button = Gtk.Button(label="Speichern")
        save_button.connect('clicked', self.save_card_changes)
        button_box.append(save_button)

        edit_box.append(button_box)

        self.content_stack.add_named(edit_box, "edit")
        self.content_stack.set_visible_child_name("edit")

    def on_card_changed(self, entry, card, field):
        """
        Handler für Änderungen an Karteikarten.
        - Markiert den Text mit Klammern und ändert die Textfarbe auf Blau.
        - Aktualisiert die Karteikarte, aber speichert sie noch nicht.
        """
        new_text = entry.get_text().strip()
        # Wenn der Text bereits markiert ist, ignorieren
        if new_text.startswith('⟨') and new_text.endswith('⟩'):
            return

        old_text = card.question if field == 'question' else card.answer

        if new_text != old_text:
            # Text mit Klammern markieren
            entry.set_text(f"⟨{new_text}⟩")
            # Textfarbe auf Blau setzen
            entry.get_style_context().add_class("modified-card")
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"entry.modified-card { color: blue; }")
            entry.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

            # Karteikarte aktualisieren aber noch nicht speichern
            if field == 'question':
                card.question = new_text
            else:
                card.answer = new_text

            # Felder für neue Eingabe vorbereiten
            entry.grab_focus()

    def on_card_delete(self, button, card, list_box, card_box):
        """
        Handler für das Löschen von Karteikarten.
        - Zeigt einen Bestätigungsdialog an.
        """
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Möchten Sie die Karteikarte '{card.question} - {card.answer}' wirklich löschen?"
        )
        dialog.connect("response", self.on_delete_confirm, card, list_box, card_box)
        dialog.show()

    def on_delete_confirm(self, dialog, response, card, list_box, card_box):
        """
        Handler für die Bestätigung des Löschens.
        - Löscht die Karteikarte aus der Datenbank und aus der Liste.
        """
        if response == Gtk.ResponseType.YES:
            try:
                # Aus der Datenbank löschen
                self.session.delete(card)
                self.session.commit()

                # Eingabefelder deaktivieren und Text durchstreichen
                for child in card_box:
                    if isinstance(child, Gtk.Entry):
                        text = child.get_text()
                        child.set_text(f"⟨{text}⟩")
                        child.set_sensitive(False)
                        child.get_style_context().add_class("deleted-card")
                        # Textfarbe auf Rot setzen
                        css_provider = Gtk.CssProvider()
                        css_provider.load_from_data(b"entry.deleted-card { color: red; }")
                        child.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

                # Aus der Liste entfernen
                list_box.remove(card_box)
            except Exception as e:
                error_dialog = Gtk.MessageDialog(
                    transient_for=dialog,
                    modal=True,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=f"Fehler beim Löschen: {str(e)}"
                )
                error_dialog.connect("response", lambda d, r: d.destroy())
                error_dialog.show()
        dialog.destroy()

    def save_card_changes(self, button):
        """
        Speichert die Änderungen in der Datenbank.
        - Speichert die Änderungen und zeigt eine Erfolgsmeldung an.
        - Zeigt eine Fehlermeldung an, wenn das Speichern fehlschlägt.
        """
        try:
            self.session.commit()
            dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Änderungen wurden gespeichert!"
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.show()
        except Exception as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=f"Fehler beim Speichern: {str(e)}"
            )
            error_dialog.connect("response", lambda d, r: d.destroy())
            error_dialog.show()

    def show_databases_menu(self, button):
        """
        Zeigt das Menü mit verfügbaren Datenbanken.
        - Leert den Content Stack und erstellt ein Datenbank-Menü.
        - Fügt eine Liste mit den verfügbaren Datenbanken hinzu.
        """
        # Hauptmenü verstecken
        self.back_button.set_visible(True)

        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Datenbank-Menü erstellen
        menu_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Verfügbare Karteikarten-Sammlungen</span>")
        menu_box.append(title_label)

        # Liste der Datenbanken
        databases = db_manager.get_available_databases()
        for db in databases:
            db_button = Gtk.Button(label=db)
            db_button.set_size_request(200, 40)
            db_button.connect("clicked", lambda b, d=db: self.show_collection_menu(d))
            menu_box.append(db_button)

        # Sammlungen verwalten Button
        if databases:  # Nur anzeigen wenn Datenbanken existieren
            manage_button = Gtk.Button(label="Karteikartensammlungen verwalten")
            manage_button.set_size_request(200, 40)
            manage_button.set_margin_top(20)
            manage_button.connect("clicked", self.show_manage_databases_dialog)
            menu_box.append(manage_button)

        self.content_stack.add_named(menu_box, "databases")
        self.content_stack.set_visible_child_name("databases")

    def show_collection_menu(self, collection_name):
        """
        Zeigt das Untermenü für eine bestimmte Karteikartensammlung.
        - Leert den Content Stack und erstellt ein Sammlung-Menü.
        - Fügt eine Liste mit den Aktionsbuttons hinzu.
        """
        # Aktualisiere die Datenbankverbindung
        self.update_database_connection(collection_name)

        self.back_button.set_visible(True)

        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Sammlung-Menü erstellen
        menu_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>{collection_name}</span>")
        menu_box.append(title_label)

        # Zurück-Pfeil
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", self.show_databases_menu)
        back_button.set_halign(Gtk.Align.START)
        menu_box.append(back_button)

        # Karteikarten neu eingeben
        new_card_button = Gtk.Button(label="Karteikarten neu eingeben")
        new_card_button.set_size_request(200, 40)
        new_card_button.connect("clicked", lambda b: self.show_add_dialog(b, collection_name))
        menu_box.append(new_card_button)

        # Karteikarten lernen
        practice_button = Gtk.Button(label="Karteikarten üben")
        practice_button.set_size_request(200, 40)
        practice_button.connect("clicked", lambda b: self.show_practice_dialog(b, collection_name))
        menu_box.append(practice_button)

        # Karteikarten bearbeiten
        edit_button = Gtk.Button(label="Karteikarten bearbeiten")
        edit_button.set_size_request(200, 40)
        edit_button.connect("clicked", lambda b: self.edit_database(b, collection_name))
        menu_box.append(edit_button)

        self.content_stack.add_named(menu_box, "collection")
        self.content_stack.set_visible_child_name("collection")

    def open_database(self, database):
        """
        Öffnet eine Datenbank.
        - Setzt die aktive Datenbank und zeigt den Inhalt an.
        """
        db_manager.set_active_database(database)
        self.show_database_content(database)

    def show_new_database_dialog(self, button):
        """
        Zeigt die Ansicht zum Erstellen einer neuen Datenbank.
        - Leert den Content Stack und erstellt eine neue Datenbank-Box.
        - Fügt ein Eingabefeld für den Datenbanknamen hinzu.
        """
        self.back_button.set_visible(True)

        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Neue Datenbank Box erstellen
        new_db_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Neue Karteikarten-Sammlung erstellen</span>")
        new_db_box.append(title_label)

        # Zurück-Pfeil
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", self.show_main_menu)
        back_button.set_halign(Gtk.Align.START)
        new_db_box.append(back_button)

        # Eingabefeld für Datenbankname
        name_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )
        name_label = Gtk.Label(label="Name der Karteikarten-Sammlung:")
        name_box.append(name_label)
        self.name_entry = Gtk.Entry()
        self.name_entry.set_hexpand(True)
        name_box.append(self.name_entry)
        new_db_box.append(name_box)

        # Buttons
        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
            margin_top=20
        )
        button_box.set_halign(Gtk.Align.CENTER)

        save_button = Gtk.Button(label="Speichern")
        save_button.connect("clicked", self.save_new_database)
        button_box.append(save_button)

        new_db_box.append(button_box)

        # Enter-Taste Handling
        self.name_entry.connect("activate", lambda w: self.save_new_database(None))

        self.content_stack.add_named(new_db_box, "new_database")
        self.content_stack.set_visible_child_name("new_database")

        # Fokus auf das erste Eingabefeld
        self.name_entry.grab_focus()

    def save_new_database(self, button):
        """
        Speichert die neue Datenbank.
        - Erstellt die neue Datenbank und zeigt eine Erfolgsmeldung an.
        - Zeigt eine Fehlermeldung an, wenn das Speichern fehlschlägt.
        """
        display_name = self.name_entry.get_text().strip()

        if display_name:
            try:
                # Der Anzeigename bleibt wie eingegeben, der Dateiname wird bereinigt
                db_name = display_name.lower().replace(' ', '_')
                db_manager.create_database(display_name, db_name)
                # Zurück zum Hauptmenü
                self.show_main_menu()
            except Exception as e:
                error_dialog = Gtk.MessageDialog(
                    transient_for=self,
                    modal=True,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=str(e)
                )
                error_dialog.connect("response", lambda d, r: d.destroy())
                error_dialog.show()
        else:
            error_dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Bitte füllen Sie alle Felder aus!"
            )
            error_dialog.connect("response", lambda d, r: d.destroy())
            error_dialog.show()

    def show_add_dialog(self, button, database_name):
        """
        Zeigt den Dialog zum Hinzufügen einer neuen Karteikarte.
        - Leert den Content Stack und erstellt einen neuen Dialog.
        - Fügt Eingabefelder für Frage und Antwort hinzu.
        """
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Dialog Box erstellen
        dialog_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>Neue Karteikarte für {database_name} erstellen</span>")
        dialog_box.append(title_label)

        # Zurück-Pfeil
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", lambda b, d=database_name: self.show_collection_menu(d))
        back_button.set_halign(Gtk.Align.START)
        dialog_box.append(back_button)

        # Frage-Box
        question_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20
        )
        dialog_box.append(question_box)

        question_label = Gtk.Label(label="Frage:")
        question_label.set_halign(Gtk.Align.START)
        question_box.append(question_label)

        question_entry = Gtk.Entry()
        question_entry.set_hexpand(True)
        question_box.append(question_entry)

        # Antwort-Box
        answer_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20
        )
        dialog_box.append(answer_box)

        answer_label = Gtk.Label(label="Antwort:")
        answer_label.set_halign(Gtk.Align.START)
        answer_box.append(answer_label)

        answer_entry = Gtk.Entry()
        answer_entry.set_hexpand(True)
        answer_box.append(answer_entry)

        # Button-Box
        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
            margin_top=20
        )
        button_box.set_halign(Gtk.Align.CENTER)

        # Abbrechen-Button
        cancel_button = Gtk.Button(label="Abbrechen")
        cancel_button.connect("clicked", self.show_main_menu)
        button_box.append(cancel_button)

        # Speichern-Button
        save_button = Gtk.Button(label="Speichern")
        save_button.connect("clicked", lambda b: self.save_and_new_card(question_entry, answer_entry, database_name))
        button_box.append(save_button)

        dialog_box.append(button_box)

        # Enter-Taste Handler für Frage-Feld
        def on_question_activate(entry):
            answer_entry.grab_focus()

        # Enter-Taste Handler für Antwort-Feld
        def on_answer_activate(entry):
            self.save_and_new_card(question_entry, answer_entry, database_name)

        # Aktivierungs-Events verbinden
        question_entry.connect("activate", on_question_activate)
        answer_entry.connect("activate", on_answer_activate)

        # Dialog zur Stack hinzufügen
        self.content_stack.add_named(dialog_box, "add_flashcard")
        self.content_stack.set_visible_child_name("add_flashcard")
        
        # Fokus auf das Frage-Feld setzen
        question_entry.grab_focus()

    def save_and_new_card(self, question_entry, answer_entry, database_name):
        """
        Speichert die aktuelle Karteikarte und bereitet die Eingabe für eine neue vor.
        """
        question = question_entry.get_text().strip()
        answer = answer_entry.get_text().strip()

        if not question or not answer:
            error_dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Bitte fülle alle Felder aus!"
            )
            error_dialog.connect("response", lambda d, r: d.destroy())
            error_dialog.show()
            return

        try:
            # Karteikarte speichern
            add_flashcard(
                self.session,
                database_name,
                question=question,
                answer=answer,
            )
            
            # Felder leeren und Fokus auf Frage setzen
            question_entry.set_text("")
            answer_entry.set_text("")
            question_entry.grab_focus()
            
        except Exception as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=f"Fehler beim Speichern: {str(e)}"
            )
            error_dialog.connect("response", lambda d, r: d.destroy())
            error_dialog.show()

    def show_practice_dialog(self, button, database_name):
        """
        Zeigt die Übungsansicht.
        - Leert den Content Stack und erstellt eine Übungs-Box.
        - Fügt eine Level-Info Box und eine Karteikarte-Box hinzu.
        """
        if not database_name:
            return

        # Aktualisiere die Datenbankverbindung
        self.update_database_connection(database_name)
        
        # Setze Start-Zeit für die Übungssession
        self.practice_start_time = datetime.now()  # Startzeit der Übungssession
        
        # Speichere den Datenbanknamen für load_next_flashcard
        self.current_database = database_name

        # Hauptmenü verstecken
        self.back_button.set_visible(True)

        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Übungs-Box erstellen
        self.practice_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>Karteikarten üben - {database_name}</span>")
        self.practice_box.append(title_label)

        # Zurück-Pfeil
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", lambda b: self.show_collection_menu(database_name))
        back_button.set_halign(Gtk.Align.START)
        self.practice_box.append(back_button)

        # Level-Info Box
        level_info_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5,
            margin_top=20,
            margin_bottom=20
        )

        # Level-Anzeige
        self.level_label = Gtk.Label()
        self.level_label.set_markup("<span size='large'>Level: -</span>")
        level_info_box.append(self.level_label)

        # Fortschritt im Level
        self.progress_label = Gtk.Label()
        self.progress_label.set_markup("<span size='small'>Richtige Antworten im Level: -</span>")
        level_info_box.append(self.progress_label)

        self.practice_box.append(level_info_box)

        # Karteikarte-Box (für Frage und optionales Bild)
        self.card_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20
        )
        self.practice_box.append(self.card_box)

        # Frage-Label
        self.question_label = Gtk.Label()
        self.question_label.set_markup("<span size='x-large'>Lade nächste Karteikarte...</span>")
        self.card_box.append(self.question_label)

        # Eingabeaufforderung
        instruction_label = Gtk.Label()
        instruction_label.set_markup("<span size='small'>Geben Sie die Antwort ein und drücken Sie Enter</span>")
        instruction_label.set_margin_top(20)
        self.card_box.append(instruction_label)

        # Eingabefeld
        self.answer_entry = Gtk.Entry()
        self.answer_entry.set_margin_top(10)
        self.answer_entry.connect("activate", self.check_answer)
        self.card_box.append(self.answer_entry)

        # Feedback-Label (für richtig/falsch Anzeige)
        self.feedback_label = Gtk.Label()
        self.feedback_label.set_margin_top(20)
        self.card_box.append(self.feedback_label)

        # Box zum Content Stack hinzufügen
        self.content_stack.add_named(self.practice_box, "practice")
        self.content_stack.set_visible_child_name("practice")

        # Erste Karteikarte laden
        self.load_next_flashcard()

    def load_next_flashcard(self):
        """
        Lädt die nächste Karteikarte zum Üben.
        - Holt die nächste Karteikarte aus der Datenbank.
        - Aktualisiert die Level-Info und die Karteikarte-Box.
        """
        # Timer stoppen, falls einer läuft
        if hasattr(self, 'next_flashcard_timer') and self.next_flashcard_timer:
            GLib.source_remove(self.next_flashcard_timer)
            self.next_flashcard_timer = None

        # Hole die nächste Karteikarte
        self.current_flashcard = get_card_for_practice(self.session, self.current_database)
        if not self.current_flashcard:
            self.question_label.set_markup(
                "<span size='large'>Keine Karteikarten zum Üben verfügbar</span>"
            )
            self.answer_entry.set_sensitive(False)
            self.level_label.set_markup("<span size='large'>Level: -</span>")
            return False

        # Level-Info aktualisieren
        self.level_label.set_markup(
            f"<span size='large'>Level: {self.current_flashcard.level}</span>"
        )
        self.progress_label.set_markup(
            f"<span size='small'>Richtige Antworten im Level: {self.current_flashcard.level_correct_count}</span>"
        )

        # Frage anzeigen
        self.question_label.set_markup(
            f"<span size='x-large'>{self.current_flashcard.question}</span>"
        )

        # Eingabefeld leeren und fokussieren
        self.answer_entry.set_text("")
        self.answer_entry.set_sensitive(True)
        self.answer_entry.grab_focus()
        self.feedback_label.set_markup("")

        return True

    def check_answer(self, widget):
        """
        Überprüft die eingegebene Antwort.
        - Überprüft, ob die Antwort richtig ist.
        - Aktualisiert die Statistiken und zeigt Feedback an.
        """
        if not hasattr(self, 'current_flashcard') or not self.current_flashcard:
            return

        # Berechne die Zeit für diese Antwort
        answer_time = datetime.now()
        practice_duration = (answer_time - self.practice_start_time).total_seconds()  # Dauer in Sekunden
        
        # Hole die eingegebene Antwort
        user_input = self.answer_entry.get_text().strip().lower()
        
        # Hole die richtige Antwort
        correct_answer = self.current_flashcard.answer.lower()
        
        # Überprüfe, ob die Antwort richtig ist
        is_correct = user_input == correct_answer
        
        # Aktualisiere die Statistiken mit Zeitstempel
        update_flashcard_stats(
            self.session, 
            self.current_flashcard.id, 
            is_correct, 
            self.current_database,
            practice_duration  # Übergebe die Übungsdauer
        )
        
        # Setze neue Startzeit für nächste Karte
        self.practice_start_time = datetime.now()
        
        # Zeige Feedback an
        if is_correct:
            self.feedback_label.set_markup(
                "<span size='large' foreground='green'>✓ Richtig!</span>"
            )
        else:
            self.feedback_label.set_markup(
                f"<span size='large' foreground='red'>✗ Falsch! Die richtige Antwort war: {self.current_flashcard.answer}</span>"
            )

        # Level und Fortschritt aktualisieren
        self.level_label.set_markup(
            f"<span size='large'>Level: {self.current_flashcard.level}</span>"
        )
        self.progress_label.set_markup(
            f"<span size='small'>Richtige Antworten im Level: {self.current_flashcard.level_correct_count}</span>"
        )

        # Starte Timer für die nächste Karteikarte
        self.next_flashcard_timer = GLib.timeout_add(2500, self.load_next_flashcard)

    def show_manage_databases_dialog(self, button):
        """
        Zeigt einen Dialog zum Verwalten der Karteikartensammlungen.
        """
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Dialog Box erstellen
        dialog_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        # Titel
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Karteikartensammlungen verwalten</span>")
        dialog_box.append(title_label)

        # Zurück-Pfeil
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", self.show_databases_menu)
        back_button.set_halign(Gtk.Align.START)
        dialog_box.append(back_button)

        # Liste der Datenbanken
        list_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20
        )
        dialog_box.append(list_box)

        databases = db_manager.get_available_databases()
        for db in databases:
            # Box für Datenbankzeile
            db_box = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=10
            )
            list_box.append(db_box)

            # Datenbankname
            name_label = Gtk.Label(label=db)
            name_label.set_hexpand(True)
            name_label.set_halign(Gtk.Align.START)
            db_box.append(name_label)

            # Umbenennen Button
            rename_button = Gtk.Button(label="Umbenennen")
            rename_button.connect("clicked", lambda b, d=db: self.show_rename_dialog(d))
            db_box.append(rename_button)

            # Löschen Button
            delete_button = Gtk.Button()
            delete_button.set_icon_name("user-trash-symbolic")
            delete_button.connect("clicked", lambda b, d=db: self.delete_database(d))
            db_box.append(delete_button)

        # Button-Box
        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
            margin_top=20
        )
        button_box.set_halign(Gtk.Align.CENTER)

        # Zurück Button
        back_button = Gtk.Button(label="Zurück")
        back_button.connect("clicked", self.show_databases_menu)
        button_box.append(back_button)

        dialog_box.append(button_box)

        self.content_stack.add_named(dialog_box, "manage_databases")
        self.content_stack.set_visible_child_name("manage_databases")

    def show_rename_dialog(self, database):
        """
        Zeigt einen Dialog zum Umbenennen einer Karteikartensammlung.
        """
        dialog = Gtk.Dialog(
            title="Karteikartensammlung umbenennen",
            transient_for=self,
            modal=True
        )
        dialog.set_default_size(400, 150)

        # Buttons hinzufügen
        cancel_button = dialog.add_button("Abbrechen", Gtk.ResponseType.CANCEL)
        rename_button = dialog.add_button("Umbenennen", Gtk.ResponseType.OK)
        
        # Box für den Dialog-Inhalt
        content_area = dialog.get_content_area()
        content_area.set_spacing(10)
        content_area.set_margin_top(10)
        content_area.set_margin_bottom(10)
        content_area.set_margin_start(10)
        content_area.set_margin_end(10)
        
        # Label für die Erklärung
        explanation = Gtk.Label()
        explanation.set_text("Wählen Sie eine Karteikartensammlung aus und geben Sie den neuen Namen ein:")
        explanation.set_halign(Gtk.Align.START)
        content_area.append(explanation)
        
        # ComboBox für die Datenbankauswahl
        db_store = Gtk.ListStore(str)
        for db in db_manager.get_available_databases():
            db_store.append([db])
        
        db_combo = Gtk.ComboBox(model=db_store)
        renderer_text = Gtk.CellRendererText()
        db_combo.pack_start(renderer_text, True)
        db_combo.add_attribute(renderer_text, "text", 0)
        
        # Setze die aktive Datenbank als Standard
        active_db = db_manager.get_active_database()
        if active_db:
            for i, row in enumerate(db_store):
                if row[0] == active_db:
                    db_combo.set_active(i)
                    break
        
        content_area.append(db_combo)
        
        # Entry für den neuen Namen
        name_entry = Gtk.Entry()
        name_entry.set_placeholder_text("Neuer Name")
        content_area.append(name_entry)
        
        def on_response(dialog, response):
            if response == Gtk.ResponseType.OK:
                selected_iter = db_combo.get_active_iter()
                if selected_iter is not None:
                    old_name = db_store[selected_iter][0]
                    new_name = name_entry.get_text().strip()
                    
                    if new_name:
                        try:
                            # Versuche die Datenbank umzubenennen
                            db_manager.rename_database(old_name, new_name)
                            
                            # Aktualisiere die Datenbankliste
                            self.update_database_list()
                            
                        except Exception as e:
                            self.show_error_dialog(str(e))
                    else:
                        self.show_error_dialog("Bitte geben Sie einen neuen Namen ein")
            
            dialog.destroy()
        
        dialog.connect("response", on_response)
        dialog.show()

    def delete_database(self, database):
        """
        Zeigt einen Bestätigungsdialog zum Löschen einer Karteikartensammlung.
        """
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=f"Möchten Sie die Karteikartensammlung '{database}' wirklich löschen?\n\nDiese Aktion kann nicht rückgängig gemacht werden!"
        )

        def on_response(dialog, response_id):
            if response_id == Gtk.ResponseType.OK:
                try:
                    db_manager.delete_database(database)
                    dialog.destroy()
                    # Dialog neu laden
                    self.show_manage_databases_dialog(None)
                except Exception as e:
                    error_dialog = Gtk.MessageDialog(
                        transient_for=dialog,
                        modal=True,
                        message_type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        text=f"Fehler beim Löschen: {str(e)}"
                    )
                    error_dialog.connect("response", lambda d, r: d.destroy())
                    error_dialog.show()
            else:
                dialog.destroy()

        dialog.connect("response", on_response)
        dialog.show()

    def show_error_dialog(self, message):
        """Zeigt einen Fehlerdialog an"""
        dialog = Gtk.Dialog(title="Fehler")
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        
        # Content Area
        content_area = dialog.get_content_area()
        content_area.set_spacing(10)
        content_area.set_margin_top(10)
        content_area.set_margin_bottom(10)
        content_area.set_margin_start(10)
        content_area.set_margin_end(10)
        
        # Message Label
        label = Gtk.Label()
        label.set_markup(message)
        label.set_wrap(True)
        content_area.append(label)
        
        # Button
        dialog.add_button("OK", Gtk.ResponseType.OK)
        
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()

    def show_info_dialog(self, title, message):
        """Zeigt einen Informationsdialog an"""
        dialog = Gtk.Dialog(title=title)
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        
        # Content Area
        content_area = dialog.get_content_area()
        content_area.set_spacing(10)
        content_area.set_margin_top(10)
        content_area.set_margin_bottom(10)
        content_area.set_margin_start(10)
        content_area.set_margin_end(10)
        
        # Message Label
        label = Gtk.Label()
        label.set_markup(message)
        label.set_wrap(True)
        content_area.append(label)
        
        # Button
        dialog.add_button("OK", Gtk.ResponseType.OK)
        
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()

    def show_reports(self, button):
        """
        Zeigt die Reports für jede Karteikartensammlung an.
        
        Bemerkungen:
        - Für jede Datenbank wird ein eigener Tab erstellt
        - Die Datenbankverbindung wird für jede Datenbank separat aktualisiert
        - Die Statistiken werden für jede Datenbank einzeln abgerufen
        - Bei fehlenden Statistiken wird eine entsprechende Meldung angezeigt
        - Die Tabs sind scrollbar, falls es viele Datenbanken gibt
        """
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)

        # Reports Box erstellen
        reports_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        reports_box.set_margin_top(20)
        reports_box.set_margin_bottom(20)
        reports_box.set_margin_start(20)
        reports_box.set_margin_end(20)

        # Überschrift
        header_label = Gtk.Label()
        header_label.set_markup("<span size='x-large'>Lernfortschritt</span>")
        reports_box.append(header_label)

        # Zurück-Pfeil
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", self.show_main_menu)
        back_button.set_halign(Gtk.Align.START)
        reports_box.append(back_button)

        # Verfügbare Datenbanken
        databases = db_manager.get_available_databases()
        if not databases:
            info_label = Gtk.Label(label="Keine Karteikartensammlungen verfügbar")
            reports_box.append(info_label)
        else:
            # Notebook (Tabs) erstellen
            notebook = Gtk.Notebook()
            notebook.set_scrollable(True)  # Ermöglicht Scrollen durch Tabs
            notebook.set_size_request(700, 500)  # Mindestgröße für das Notebook
            
            # Für jede Datenbank einen Tab erstellen
            for db in databases:
                # Datenbankverbindung für diese Datenbank aktualisieren
                self.update_database_connection(db)
                
                # Hole die Statistiken für diese Datenbank
                stats = get_database_stats(self.session, db)
                
                # Scrollbare Box für den Tab-Inhalt
                scrolled = Gtk.ScrolledWindow()
                scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
                scrolled.set_size_request(680, 450)  # Größe für die ScrolledWindow
                
                # Box für den Tab-Inhalt
                db_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                db_box.set_margin_top(10)
                db_box.set_margin_bottom(10)
                db_box.set_margin_start(20)  # Mehr Platz an den Seiten
                db_box.set_margin_end(20)
                db_box.set_size_request(640, -1)  # Breite festlegen, Höhe automatisch
                
                # Datenbankname als Überschrift
                db_label = Gtk.Label()
                db_label.set_markup(f"<span size='large' weight='bold'>{db}</span>")
                db_label.set_halign(Gtk.Align.START)
                db_box.append(db_label)

                # Statistiken für diese Datenbank
                if db in stats:
                    db_stats = stats[db]
                    stats_text = (
                        f"<span size='large' weight='bold'>Karteikarten:</span>\n"
                        f"Gesamt: {db_stats['total_cards']}\n"
                        f"Level 1: {db_stats['cards_per_level'][1]}\n"
                        f"Level 2: {db_stats['cards_per_level'][2]}\n"
                        f"Level 3: {db_stats['cards_per_level'][3]}\n"
                        f"Level 4: {db_stats['cards_per_level'][4]}\n\n"
                    )
                    
                    # Übungsstatistiken für verschiedene Zeiträume
                    time_ranges = ['last_7_days', 'last_30_days', 'last_365_days', 'all_time']
                    time_range_names = {
                        'last_7_days': 'Letzte 7 Tage',
                        'last_30_days': 'Letzte 30 Tage',
                        'last_365_days': 'Letztes Jahr',
                        'all_time': 'Gesamt'
                    }
                    
                    for time_range in time_ranges:
                        stats_range = db_stats['practice_stats'][time_range]
                        stats_text += (
                            f"\n<span size='large' weight='bold'>{time_range_names[time_range]}:</span>\n"
                            f"Übungsversuche: {stats_range['attempts']}\n"
                            f"Korrekte Antworten: {stats_range['correct']}\n"
                            f"Erfolgsquote: {stats_range['success_rate']:.1f}%\n"
                        )
                        
                        # Formatiere die Übungszeit
                        total_minutes = stats_range['duration'] / 60
                        if total_minutes >= 60:
                            hours = int(total_minutes // 60)
                            minutes = int(total_minutes % 60)
                            stats_text += f"Gesamte Übungszeit: {hours}h {minutes}m\n"
                        else:
                            stats_text += f"Gesamte Übungszeit: {int(total_minutes)}m\n"
                        
                        if stats_range['attempts'] > 0:
                            avg_seconds = stats_range['avg_duration']
                            stats_text += f"Durchschnittliche Zeit pro Karte: {int(avg_seconds)}s\n"
                    
                    stats_label = Gtk.Label()
                    stats_label.set_markup(stats_text)
                    stats_label.set_halign(Gtk.Align.START)
                    db_box.append(stats_label)
                else:
                    # Keine Statistiken verfügbar
                    no_stats_label = Gtk.Label(label="Keine Statistiken verfügbar")
                    no_stats_label.set_halign(Gtk.Align.START)
                    db_box.append(no_stats_label)

                # Box in ScrolledWindow packen
                scrolled.set_child(db_box)
                
                # Tab-Label erstellen
                tab_label = Gtk.Label(label=db)
                
                # Tab zum Notebook hinzufügen
                notebook.append_page(scrolled, tab_label)

            # Notebook zur Reports Box hinzufügen
            reports_box.append(notebook)

        # Reports Box zum Stack hinzufügen
        self.content_stack.add_named(reports_box, "reports")
        self.content_stack.set_visible_child_name("reports")

    def update_database_connection(self, database_name=None):
        """
        Aktualisiert die Datenbankverbindung für die angegebene Datenbank.
        Wenn keine Datenbank angegeben ist, wird die aktive Datenbank verwendet.
        """
        try:
            # Bestimme die zu verwendende Datenbank
            if database_name is None:
                database_name = db_manager.get_active_database()
            
            if database_name:
                # Aktualisiere die Datenbankstruktur
                update_database_structure(database_name)
                
                # Hole den Pfad zur Datenbank
                db_path = db_manager.get_db_path(database_name)
                
                # Erstelle die Engine und Session
                engine = create_engine(f'sqlite:///{db_path}')
                Base.metadata.create_all(engine)  # Erstelle fehlende Tabellen
                
                Session = sessionmaker(bind=engine)
                
                # Schließe alte Session falls vorhanden
                if hasattr(self, 'session'):
                    self.session.close()
                    
                # Erstelle neue Session
                self.session = Session()
                
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Datenbankverbindung: {str(e)}")
            raise

class FlashcardTrainerApp(Adw.Application):
    """
    Hauptanwendung.
    """
    def __init__(self, **kwargs):
        """
        Initialisiert die Hauptanwendung.
        - Verbindet die activate-Signal mit der on_activate-Methode.
        """
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        """
        Aktiviert die Hauptanwendung.
        - Erstellt ein neues Hauptfenster und zeigt es an.
        """
        self.win = MainWindow(application=app)
        self.win.present()


def main():
    """
    Hauptfunktion.
    - Erstellt eine neue Hauptanwendung und startet sie.
    """
    app = FlashcardTrainerApp(application_id="org.example.klar")
    return app.run()


if __name__ == "__main__":
    main()
