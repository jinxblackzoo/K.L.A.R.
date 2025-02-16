"""
M.U.T. - Mathematische Umrechnungen Trainieren
Datenbank für SI-Einheiten und deren Umrechnungen
"""

#######################
# Längeneinheiten
#######################
LENGTH_UNITS = {
    "km": {
        "name": "Kilometer",
        "base_unit": "m",
        "factor": 1000,
        "example": "Damit misst du zum Beispiel die Entfernung zwischen zwei Städten",
        "hint": "1 km = 1000 m (× 1000)"
    },
    "m": {
        "name": "Meter",
        "base_unit": "m",
        "factor": 1,
        "example": "Damit misst du zum Beispiel die Länge eines Fußballfeldes",
        "hint": "1 m = 100 cm (× 100)"
    },
    "dm": {
        "name": "Dezimeter",
        "base_unit": "m",
        "factor": 0.1,
        "example": "Damit misst du zum Beispiel die Länge deines Lineals",
        "hint": "1 dm = 10 cm (× 10)"
    },
    "cm": {
        "name": "Zentimeter",
        "base_unit": "m",
        "factor": 0.01,
        "example": "Damit misst du zum Beispiel die Länge deines Bleistifts",
        "hint": "1 cm = 10 mm (× 10)"
    },
    "mm": {
        "name": "Millimeter",
        "base_unit": "m",
        "factor": 0.001,
        "example": "Damit misst du zum Beispiel die Dicke eines Blattes Papier",
        "hint": "1 mm ist die kleinste Längeneinheit hier"
    }
}

#######################
# Volumeneinheiten
#######################
VOLUME_UNITS = {
    "m³": {
        "name": "Kubikmeter",
        "base_unit": "m³",
        "factor": 1,
        "example": "Damit misst du zum Beispiel wie viel Wasser in ein Schwimmbecken passt",
        "hint": "1 m³ = 1000 l (× 1000)"
    },
    "dm³": {
        "name": "Kubikdezimeter",
        "base_unit": "m³",
        "factor": 0.001,
        "example": "Damit misst du zum Beispiel wie viel Wasser in eine große Flasche passt",
        "hint": "1 dm³ = 1 l (gleich groß)"
    },
    "cm³": {
        "name": "Kubikzentimeter",
        "base_unit": "m³",
        "factor": 0.000001,
        "example": "Damit misst du zum Beispiel wie viel Wasser in einen Würfel mit 1cm Kantenlänge passt",
        "hint": "1 cm³ = 1 ml (gleich groß)"
    },
    "l": {
        "name": "Liter",
        "base_unit": "m³",
        "factor": 0.001,
        "example": "Damit misst du zum Beispiel wie viel Saft in einer Flasche ist",
        "hint": "1 l = 1000 ml (× 1000)"
    },
    "ml": {
        "name": "Milliliter",
        "base_unit": "m³",
        "factor": 0.000001,
        "example": "Wenn du kochst und Flüssigkeiten misst, nutzt du diese Einheit",
        "hint": "1 ml = 1 cm³ (gleich groß)"
    }
}

#######################
# Zeiteinheiten
#######################
TIME_UNITS = {
    "h": {
        "name": "Stunden",
        "base_unit": "s",
        "factor": 3600,
        "example": "Damit misst du zum Beispiel wie lange ein Schultag dauert",
        "hint": "1 h = 60 min (× 60)"
    },
    "min": {
        "name": "Minuten",
        "base_unit": "s",
        "factor": 60,
        "example": "Damit misst du zum Beispiel wie lange eine Schulstunde dauert",
        "hint": "1 min = 60 s (× 60)"
    },
    "s": {
        "name": "Sekunden",
        "base_unit": "s",
        "factor": 1,
        "example": "Damit misst du zum Beispiel wie lange du brauchst, um von 1 bis 10 zu zählen",
        "hint": "1 s ist die kleinste Zeiteinheit hier"
    }
}

#######################
# Flächeneinheiten
#######################
AREA_UNITS = {
    "km²": {
        "name": "Quadratkilometer",
        "base_unit": "m²",
        "factor": 1000000,
        "example": "Damit misst du zum Beispiel die Fläche einer Stadt",
        "hint": "1 km² = 1.000.000 m² (× 1.000.000)"
    },
    "ha": {
        "name": "Hektar",
        "base_unit": "m²",
        "factor": 10000,
        "example": "Damit misst du zum Beispiel die Größe eines Bauernhofs",
        "hint": "1 ha = 10.000 m² (× 10.000)"
    },
    "m²": {
        "name": "Quadratmeter",
        "base_unit": "m²",
        "factor": 1,
        "example": "Damit misst du zum Beispiel die Größe deines Zimmers",
        "hint": "1 m² = 100 dm² (× 100)"
    },
    "dm²": {
        "name": "Quadratdezimeter",
        "base_unit": "m²",
        "factor": 0.01,
        "example": "Damit misst du zum Beispiel die Fläche eines DIN A4 Blattes",
        "hint": "1 dm² = 100 cm² (× 100)"
    },
    "cm²": {
        "name": "Quadratzentimeter",
        "base_unit": "m²",
        "factor": 0.0001,
        "example": "Damit misst du zum Beispiel die Fläche eines Briefmarkens",
        "hint": "1 cm² = 100 mm² (× 100)"
    },
    "mm²": {
        "name": "Quadratmillimeter",
        "base_unit": "m²",
        "factor": 0.000001,
        "example": "Damit misst du zum Beispiel sehr kleine Flächen wie einen Punkt auf dem Papier",
        "hint": "1 mm² ist die kleinste Flächeneinheit hier"
    }
}

#######################
# Masseneinheiten
#######################
MASS_UNITS = {
    "t": {
        "name": "Tonne",
        "base_unit": "kg",
        "factor": 1000,
        "example": "Damit wiegst du zum Beispiel einen kleinen LKW",
        "hint": "1 t = 1000 kg (× 1000)"
    },
    "kg": {
        "name": "Kilogramm",
        "base_unit": "kg",
        "factor": 1,
        "example": "Damit wiegst du zum Beispiel einen Sack Kartoffeln",
        "hint": "1 kg = 1000 g (× 1000)"
    },
    "g": {
        "name": "Gramm",
        "base_unit": "kg",
        "factor": 0.001,
        "example": "Damit wiegst du zum Beispiel eine Tafel Schokolade",
        "hint": "1 g = 1000 mg (× 1000)"
    },
    "mg": {
        "name": "Milligramm",
        "base_unit": "kg",
        "factor": 0.000001,
        "example": "Damit wiegst du zum Beispiel eine Tablette",
        "hint": "1 mg ist die kleinste Masseneinheit hier"
    }
}

#######################
# Geschwindigkeitseinheiten
#######################
SPEED_UNITS = {
    "km/h": {
        "name": "Kilometer pro Stunde",
        "base_unit": "m/s",
        "factor": 0.277778,  # 1 km/h = 0.277778 m/s
        "example": "Damit misst du zum Beispiel die Geschwindigkeit eines Autos",
        "hint": "1 km/h ≈ 0,28 m/s (÷ 3,6)"
    },
    "m/s": {
        "name": "Meter pro Sekunde",
        "base_unit": "m/s",
        "factor": 1,
        "example": "Damit misst du zum Beispiel die Geschwindigkeit eines fallenden Balls",
        "hint": "1 m/s = 3,6 km/h (× 3,6)"
    }
}

#######################
# Temperatureinheiten
#######################
TEMPERATURE_UNITS = {
    "K": {
        "name": "Kelvin",
        "base_unit": "K",
        "factor": 1,
        "example": "Damit misst du zum Beispiel die absolute Temperatur im Weltall",
        "hint": "0 K = -273,15 °C (absoluter Nullpunkt)"
    },
    "°C": {
        "name": "Grad Celsius",
        "base_unit": "K",
        "factor": 1,
        "offset": 273.15,  # 0°C = 273.15K
        "example": "Damit misst du zum Beispiel die Temperatur draußen",
        "hint": "0 °C = Gefrierpunkt von Wasser"
    },
    "°F": {
        "name": "Grad Fahrenheit",
        "base_unit": "K",
        "factor": 0.555556,  # (°F - 32) * 5/9 + 273.15 = K
        "offset": 255.372,  # 0°F = 255.372K
        "example": "Damit wird die Temperatur in den USA gemessen",
        "hint": "0 °F = -17,8 °C"
    }
}

#######################
# Druckeinheiten
#######################
PRESSURE_UNITS = {
    "bar": {
        "name": "Bar",
        "base_unit": "Pa",
        "factor": 100000,
        "example": "Damit misst du zum Beispiel den Luftdruck in Autoreifen",
        "hint": "1 bar = 100.000 Pa (× 100.000)"
    },
    "hPa": {
        "name": "Hektopascal",
        "base_unit": "Pa",
        "factor": 100,
        "example": "Damit wird der Luftdruck in der Wettervorhersage angegeben",
        "hint": "1 hPa = 100 Pa (× 100)"
    },
    "Pa": {
        "name": "Pascal",
        "base_unit": "Pa",
        "factor": 1,
        "example": "Die Grundeinheit des Drucks",
        "hint": "1 Pa = 1 N/m²"
    }
}

#######################
# Energieeinheiten
#######################
ENERGY_UNITS = {
    "kWh": {
        "name": "Kilowattstunde",
        "base_unit": "J",
        "factor": 3600000,
        "example": "Damit wird dein Stromverbrauch gemessen",
        "hint": "1 kWh = 3.600.000 J (× 3.600.000)"
    },
    "kJ": {
        "name": "Kilojoule",
        "base_unit": "J",
        "factor": 1000,
        "example": "Damit wird der Energiegehalt von Lebensmitteln angegeben",
        "hint": "1 kJ = 1000 J (× 1000)"
    },
    "J": {
        "name": "Joule",
        "base_unit": "J",
        "factor": 1,
        "example": "Die Grundeinheit der Energie",
        "hint": "1 J = 1 Wattsekunde"
    }
}

#######################
# Leistungseinheiten
#######################
POWER_UNITS = {
    "kW": {
        "name": "Kilowatt",
        "base_unit": "W",
        "factor": 1000,
        "example": "Damit wird zum Beispiel die Leistung eines Autos angegeben",
        "hint": "1 kW = 1000 W (× 1000)"
    },
    "W": {
        "name": "Watt",
        "base_unit": "W",
        "factor": 1,
        "example": "Damit wird zum Beispiel die Leistung einer Glühbirne angegeben",
        "hint": "1 W = 1 Joule pro Sekunde"
    }
}

#######################
# Elektrische Einheiten
#######################
ELECTRIC_UNITS = {
    "kV": {
        "name": "Kilovolt",
        "base_unit": "V",
        "factor": 1000,
        "example": "Damit wird die Spannung in Hochspannungsleitungen gemessen",
        "hint": "1 kV = 1000 V (× 1000)"
    },
    "V": {
        "name": "Volt",
        "base_unit": "V",
        "factor": 1,
        "example": "Damit wird zum Beispiel die Spannung einer Batterie gemessen",
        "hint": "1 V = Spannung einer AA-Batterie"
    },
    "mV": {
        "name": "Millivolt",
        "base_unit": "V",
        "factor": 0.001,
        "example": "Damit werden sehr kleine Spannungen gemessen",
        "hint": "1 mV = 0,001 V (÷ 1000)"
    },
    "A": {
        "name": "Ampere",
        "base_unit": "A",
        "factor": 1,
        "example": "Damit wird die Stromstärke gemessen",
        "hint": "1 A = 1 Coulomb pro Sekunde"
    },
    "mA": {
        "name": "Milliampere",
        "base_unit": "A",
        "factor": 0.001,
        "example": "Damit wird zum Beispiel der Stromverbrauch eines Handys gemessen",
        "hint": "1 mA = 0,001 A (÷ 1000)"
    },
    "Ω": {
        "name": "Ohm",
        "base_unit": "Ω",
        "factor": 1,
        "example": "Damit wird der elektrische Widerstand gemessen",
        "hint": "1 Ω = 1 Volt pro Ampere"
    },
    "kΩ": {
        "name": "Kiloohm",
        "base_unit": "Ω",
        "factor": 1000,
        "example": "Damit werden größere Widerstände gemessen",
        "hint": "1 kΩ = 1000 Ω (× 1000)"
    }
}

# Zusammenfassung aller Einheiten nach Kategorie
SI_UNITS = {
    "length": {
        "name": "Längeneinheiten",
        "description": "Einheiten für Längen und Strecken",
        "units": LENGTH_UNITS
    },
    "area": {
        "name": "Flächeneinheiten",
        "description": "Einheiten für Flächen",
        "units": AREA_UNITS
    },
    "volume": {
        "name": "Volumeneinheiten",
        "description": "Einheiten für Rauminhalte und Volumen",
        "units": VOLUME_UNITS
    },
    "time": {
        "name": "Zeiteinheiten",
        "description": "Einheiten für Zeitspannen",
        "units": TIME_UNITS
    },
    "mass": {
        "name": "Masseneinheiten",
        "description": "Einheiten für Masse",
        "units": MASS_UNITS
    },
    "speed": {
        "name": "Geschwindigkeitseinheiten",
        "description": "Einheiten für Geschwindigkeit",
        "units": SPEED_UNITS
    },
    "temperature": {
        "name": "Temperatureinheiten",
        "description": "Einheiten für Temperatur",
        "units": TEMPERATURE_UNITS
    },
    "pressure": {
        "name": "Druckeinheiten",
        "description": "Einheiten für Druck",
        "units": PRESSURE_UNITS
    },
    "energy": {
        "name": "Energieeinheiten",
        "description": "Einheiten für Energie",
        "units": ENERGY_UNITS
    },
    "power": {
        "name": "Leistungseinheiten",
        "description": "Einheiten für Leistung",
        "units": POWER_UNITS
    },
    "electric": {
        "name": "Elektrische Einheiten",
        "description": "Einheiten für Elektrizität",
        "units": ELECTRIC_UNITS
    }
}

def get_unit_info(category, unit):
    """
    Gibt Informationen zu einer bestimmten Einheit zurück.
    """
    try:
        return SI_UNITS[category]["units"][unit]
    except KeyError:
        return None

def get_conversion_factor(from_unit, to_unit):
    """
    Berechnet den Umrechnungsfaktor zwischen zwei Einheiten.
    
    Args:
        from_unit (str): Ausgangseinheit
        to_unit (str): Zieleinheit
    
    Returns:
        tuple: (factor, offset) für die Umrechnung
               Bei normalen Einheiten ist offset = 0
               Bei Temperatureinheiten wird offset benötigt
    
    Beispiele:
        get_conversion_factor('km', 'm') -> (1000, 0)     # 1 km = 1000 m
        get_conversion_factor('°C', 'K') -> (1, 273.15)   # °C = K - 273.15
        get_conversion_factor('°F', '°C') -> (5/9, -17.8) # (°F - 32) * 5/9 = °C
    """
    # Finde die Kategorie der Einheiten
    category = None
    for cat, info in SI_UNITS.items():
        if from_unit in info['units'] and to_unit in info['units']:
            category = cat
            break
    
    if category is None:
        raise ValueError(f"Einheiten {from_unit} und {to_unit} nicht in der gleichen Kategorie gefunden!")

    # Spezialfall: Temperatureinheiten
    if category == "temperature":
        # Umrechnung in Kelvin
        if from_unit == "K":
            from_factor = 1
            from_offset = 0
        elif from_unit == "°C":
            from_factor = 1
            from_offset = 273.15
        elif from_unit == "°F":
            from_factor = 5/9
            from_offset = 255.372  # (32°F - 32) * 5/9 + 273.15

        # Umrechnung von Kelvin
        if to_unit == "K":
            to_factor = 1
            to_offset = 0
        elif to_unit == "°C":
            to_factor = 1
            to_offset = -273.15
        elif to_unit == "°F":
            to_factor = 9/5
            to_offset = -459.67

        return (from_factor * to_factor, to_offset)

    # Normale Einheiten: Einfache Multiplikation
    from_factor = SI_UNITS[category]['units'][from_unit]['factor']
    to_factor = SI_UNITS[category]['units'][to_unit]['factor']
    
    return (from_factor / to_factor, 0)

def convert_value(value, from_unit, to_unit):
    """
    Rechnet einen Wert von einer Einheit in eine andere um.
    
    Args:
        value (float): Der umzurechnende Wert
        from_unit (str): Ausgangseinheit
        to_unit (str): Zieleinheit
    
    Returns:
        float: Der umgerechnete Wert
    
    Beispiele:
        convert_value(1, 'km', 'm') -> 1000     # 1 km = 1000 m
        convert_value(0, '°C', 'K') -> 273.15   # 0°C = 273.15 K
        convert_value(32, '°F', '°C') -> 0      # 32°F = 0°C
    """
    factor, offset = get_conversion_factor(from_unit, to_unit)
    
    # Bei Temperatureinheiten
    if offset != 0:
        if from_unit == "°F":
            # Erst in Celsius umrechnen
            value = (value - 32) * factor
        else:
            value = value * factor
        
        # Dann den Offset anwenden
        value = value + offset
    else:
        # Normale Einheiten: Einfache Multiplikation
        value = value * factor
    
    return value

def get_random_conversion(category=None):
    """
    Generiert eine zufällige Umrechnungsaufgabe.
    
    Args:
        category (str): Optional, die Kategorie für die Aufgabe.
                       Wenn None, wird eine zufällige Kategorie gewählt.
    
    Returns:
        dict: Ein Dictionary mit den Aufgabeninformationen
    """
    import random

    # Wähle eine zufällige Kategorie wenn keine angegeben
    if category is None:
        category = random.choice(list(SI_UNITS.keys()))
    
    # Hole die verfügbaren Einheiten für diese Kategorie
    units = list(SI_UNITS[category]['units'].keys())
    
    # Wähle zufällig zwei verschiedene Einheiten
    from_unit = random.choice(units)
    to_unit = random.choice([u for u in units if u != from_unit])
    
    # Generiere einen zufälligen Wert basierend auf der Kategorie
    if category == "temperature":
        value = random.randint(-50, 100)  # Realistische Temperaturen
    elif category == "mass":
        value = random.randint(1, 1000)   # 1-1000 für Massen
    elif category == "length":
        value = random.randint(1, 100)    # 1-100 für Längen
    elif category == "area":
        if from_unit == "km²":
            value = random.randint(1, 10)  # 1-10 km² (realistisch für kleine Städte)
        elif from_unit == "ha":
            value = random.randint(1, 100) # 1-100 ha (realistisch für Felder)
        elif from_unit == "m²":
            value = random.randint(1, 1000) # 1-1000 m² (realistisch für Grundstücke)
        else:
            value = random.randint(1, 100) # 1-100 für kleinere Flächeneinheiten
    elif category == "volume":
        value = random.randint(1, 20)     # 1-20 für Volumen
    elif category == "time":
        value = random.randint(1, 60)     # 1-60 für Zeiten
    elif category == "speed":
        value = random.randint(1, 120)    # 1-120 für Geschwindigkeiten
    else:
        value = random.randint(1, 100)    # Standardbereich
    
    # Füge manchmal Dezimalstellen hinzu
    if random.random() < 0.3:  # 30% Chance
        value += round(random.random(), 2)
    
    return {
        'value': value,
        'from_unit': from_unit,
        'to_unit': to_unit,
        'category': category
    }
