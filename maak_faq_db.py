import sqlite3

# Verbind met (of maak) de database
conn = sqlite3.connect("faq.db")
cursor = conn.cursor()

# Maak de tabel aan
cursor.execute("""
CREATE TABLE IF NOT EXISTS faq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vraag TEXT NOT NULL,
    antwoord TEXT NOT NULL
)
""")

# Voeg voorbeeldvragen toe
faq_data = [
    ("Wat zijn jullie openingstijden?", "We zijn geopend van maandag tot en met vrijdag van 09:00 tot 17:00."),
    ("Hoe neem ik contact op?", "Stuur een e-mail naar zierick@jumptechit.nl of bel 0123-456789."),
    ("Waar is jullie kantoor gevestigd?", "Ons kantoor bevindt zich aan de Hoofdstraat 123 in Eindhoven."),
    ("Bieden jullie ook support aan?", "Ja, we bieden support via e-mail en telefoon."),
    ("Hoe kan ik een afspraak maken?", "Je kunt een afspraak maken via onze website of telefonisch."),
    ("Hebben jullie een nieuwsbrief?", "Ja, meld je aan via onze website."),
    ("Wat zijn jullie betaalmogelijkheden?", "We accepteren iDEAL, PayPal en creditcard."),
    ("Kan ik mijn bestelling retourneren?", "Ja, binnen 14 dagen mits ongebruikt."),
    ("Zijn jullie producten duurzaam?", "Ja, duurzaamheid staat bij ons centraal."),
    ("Werken jullie ook op locatie?", "Ja, we werken zowel op afstand als op locatie.")
]

cursor.executemany("INSERT INTO faq (vraag, antwoord) VALUES (?, ?)", faq_data)

# Opslaan en sluiten
conn.commit()
conn.close()

print("✅ Database 'faq.db' is aangemaakt en gevuld.")
