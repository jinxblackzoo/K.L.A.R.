# Entwicklungsplan: K.L.A.R. - Karteikarten Lernen Aber Richtig
# Unterprojekt: M.U.T. Mathematische Umrechnungen Trainieren. SI-Einheiten umrechnen üben

# GUI 
[]	Menüpunkt: M.U.T. zum Hauptmenü von K.L.A.R. hinzufügen
	[] Untermenü: Button Starte Lernsession
	[] Wilkommenstext: "Wilkommen bei M.U.T. Mathematische Umrechnungen Trainieren"\n "Du kannst das, nur Mut :-)"
	[] Bei Klick von Button "Starte Lernsession" starte Timer um Dauer und Datum der Lernsession zu protokollieren
	[] Ein Feld für eine vom Programm generierte SI-Einheiten Vorgabe und die Aufforderung diese in eine andere Einheit umzurechnen (Beispiel: Bitte rechne 1,5m³ in Liter um.) 	
	[] Ein Feld in der die Antwort (Zahl mit korrekter SI-Einheit) eingegeben werden kann 
	[] "Beende Lernsession" Button mit der Funktion ins Hauptmenü zurückzukehren, den Timer zu stoppen und die Reportingfunktion zu aktualisieren. Nutze dafür die bereits vorhandene Reportingfunktion von K.L.A.R.
	
# Funktion der Lernsession
[] 	Anlegen einer Datenbank, welche nicht über die GUI zu bearbeiten ist. Diese soll vom Entwickler über Github aktualisiert werden
	[] Anlegen von SI-Einheiten und deren Umrechnungen. Zum Beispiel m³ in dm³ oder Liter, dm³/Liter in cm³, m in cm, dm in mm, sek in min, m² in km² 
[]  Das Programm entwickelt einen Frage-Antwort Mechanismus nach dem Zufallsprinzip
	[] Frage: Bitte rechne "Zahl mit maximal 3 Nachkommastellen und 5 ganzen Zahlen"+ "SI-Einheit aus der Datenbank" in "passende SI-Einheit" um.
	[] Antwort: Prüfe ob die Eingegebene Zahl und SI-Einheit korrekt ist
	[] Rückmeldung ob die Antwort falsch oder korrekt ist
		[] Falsch: Roter Schriftzug und X
		[] Richtig: Grüner Schriftzug und Haken
		[] Rückmeldung an Reportingfunktion mit Zeitstempel DD:MM:YYYY HH:MM
	[] Reporting beim Beenden der Lernsession mit Zeitstempel DD:MM:YYYY HH:MM an die Reportingfunktion 
	  
# Reporting
[]	Übernahme der bereits implementierten Funktionen aus K.L.A.R.	
[]	Protokollieren und sammeln der Zeitstempel (DD:MM:YYYY HH:MM) pro Lernsession
[]	Auswerten und Anzeigen der Lernsessions in eigenem M.U.T.-Tab im "Report" nach dem Prinzip von K.L.A.R.  
	 
