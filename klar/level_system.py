# Diese Datei ist für das Level-System zustændig.

# Priorisierung

    # Level 1
        # Neue eingegebene Karteikarten
        
        # Gewichtung 4
        
        # Priorität: sehr hoch
    
    
    # Level 2
        # Karteikarten, die 4x richtig beantwortet wurden
        
        # Gewichtung 3
        
        # Priorität: hoch
    
    
    # Level 3
        # Karteikarten, die 6x im Level 2 richtig beantwortet wurden
        
        # Gewichtung 2
        
        # Priorität: normal
    
    
    # Level 4
        # Karteikarten, die 10x im Level 3 richtig beantwortet wurden
        
        # Gewichtung 1
        
        # Priorität: niedrig

# Hochstufung

    # Level 1 Hochstufung auf Level 2 bei 4 richtigen Antworten 
    
    # Level 2 Hochstufung auf Level 3 bei 6 richtigen Antworten 
    
    # Level 3 Hochstufung auf Level 4 bei 10 richtigen Antworten 
    
    # Level 4: Karteikarte bleibt auf dem Level und wird weiterhin regelmäßig nach der Gewichtung und dem Zufallsprinzip abgefragt. Abfrage nach dem Zufallsprinzip mit der Gewichtung 1

# Rückstufung

    # Level 1: 1 Fehlversuch → Erhöhung der Abfragefrequenz um Faktor 2

    # Level 2: 1 Fehlversuch → Rückstufung auf Level 1

    # Level 3: 2 Fehlversuche → Rückstufung auf Level 2

    # Level 4: 2 Fehlversuche → Rückstufung auf Level 3


# Abfragefrequenz

    # Level 1: Mindestens 5 Zufallsabfragen
    
    # Level 2: Mindestens 10 Zufallsabfragen
    
    # Level 3: Mindestens 15 Zufallsabfragen
    
    # Level 4: Zufallsabfragen, bei richtiger Antwort bleibt das Level
