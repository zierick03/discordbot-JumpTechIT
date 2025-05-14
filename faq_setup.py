#dit bestand maakt database aan draai 1 keer

import sqlite3

conn = sqlite3.connect("faq.db")
cursor = conn.cursor()

# Maak tabel aan
cursor.execute("""
CREATE TABLE IF NOT EXISTS faq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vraag TEXT NOT NULL,
    antwoord TEXT NOT NULL
)
""")

# Voeg voorbeeldvragen toe
faq_items = [
    ("Wat is JumpTech-IT?", "JumpTech-IT is een IT-bedrijf gericht op innovatie."),
    ("Hoe neem ik contact op?", "Je kunt mailen naar zierick@jumptechit.nl."),
    ("Waar is het bedrijf gevestigd?", "JumpTech-IT is gevestigd in Nederland."),
    ("Wat doet de bot?", "De bot helpt je met info, tools en services."),
    ("Is deze bot open source?", "Nee, deze bot is een intern project."),
    ("Wie heeft deze bot gemaakt?", "De bot is gemaakt door Zierick."),
    ("Hoe kan ik een bug melden?", "Stuur een bericht via Discord of mail."),
    ("Is er een website?", "Ja, binnenkort op www.jumptechit.nl."),
    ("Hoe vaak wordt de bot geüpdatet?", "Wekelijks met nieuwe functies."),
    ("Hoe kan ik me aanmelden voor JumpTech-IT?", "Via het contactformulier op de website.")
]

cursor.executemany("INSERT INTO faq (vraag, antwoord) VALUES (?, ?)", faq_items)
conn.commit()
conn.close()
