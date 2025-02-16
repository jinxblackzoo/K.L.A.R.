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

from klar.gui import FlashcardTrainerApp

def main():
    app = FlashcardTrainerApp(application_id="de.blackzoo.klar")
    return app.run(None)

if __name__ == "__main__":
    main()
