#pip install discord.py (uitvoeren in powershell)
#pip install discord.py

import discord
import random
import sqlite3
from discord.ext import commands


# Bot setup met intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=["/", "!"], intents=intents)

# Event: Bot is online
@bot.event
async def on_ready():
    print(f'✅ Bot is online als: {bot.user}')
    await bot.tree.sync()  # Zorg ervoor dat de slash-commando's worden gesynchroniseerd
    print("Slash-commando's zijn gesynchroniseerd!")

# Normale (prefix) commando's
@bot.command()
async def hoi(ctx):
    await ctx.send(f'Hoi {ctx.author.mention}! 👋')

@bot.command()
async def hallo(ctx):
    await ctx.send(f'Hallo {ctx.author.mention}, hoe gaat het? 😄')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.command()
async def randomgetal(ctx, start: int, einde: int):
    import random
    getal = random.randint(start, einde)
    await ctx.send(f'Het willekeurige getal tussen {start} en {einde} is: {getal}')

# Slash-commando's (werkt met / in Discord)
@bot.tree.command(name="hoi", description="Zegt hoi tegen de gebruiker")
async def hoi(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hoi {interaction.user.mention}! 👋')

@bot.tree.command(name="hallo", description="Groet de gebruiker")
async def hallo(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hallo {interaction.user.mention}, hoe gaat het? 😄')

@bot.tree.command(name="ping", description="Test de bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.tree.command(name="randomgetal", description="Geef een willekeurig getal tussen start en einde")
async def randomgetal(interaction: discord.Interaction, start: int, einde: int):
    import random
    getal = random.randint(start, einde)
    await interaction.response.send_message(f'Het willekeurige getal tussen {start} en {einde} is: {getal}')

# Slash-commando voor contact
@bot.tree.command(name="contact", description="Geef contactinformatie")
async def contact(interaction: discord.Interaction):
    contact_info = """
    Neem contact op met ons via de volgende kanalen:
    📧 E-mail: zierick@jumptechit.nl
    📱 Telefoon: 06-38273136
        Instagram JumpTechIT
        linkedin  Jumptech-it
    """
    await interaction.response.send_message(contact_info)
    
    # Slash-commando: FAQ lijst tonen
@bot.tree.command(name="faq", description="Toon een lijst met veelgestelde vragen")
async def faq(interaction: discord.Interaction):
    # Verbind met SQLite database
    conn = sqlite3.connect("faq.db")
    cursor = conn.cursor()

    # Haal alle vragen op uit de FAQ-tabel
    cursor.execute("SELECT id, vraag FROM faq")
    vragen = cursor.fetchall()
    conn.close()

    # Check of er vragen zijn gevonden
    if not vragen:
        await interaction.response.send_message("Er zijn momenteel geen FAQ-vragen beschikbaar.")
        return

    # Bouw het antwoord op met alle vragen
    antwoord = "**Veelgestelde Vragen (FAQ):**\n"
    for id, vraag in vragen:
        antwoord += f"{id}. {vraag}\n"

    # Voeg instructie toe
    antwoord += "\nGebruik `/faq_antwoord <nummer>` om het antwoord te zien."

    # Stuur de lijst met vragen naar Discord
    await interaction.response.send_message(antwoord)

# Slash-commando: Antwoord op een specifieke vraag opvragen
@bot.tree.command(name="faq_antwoord", description="Geef antwoord op een specifieke FAQ-vraag")
async def faq_antwoord(interaction: discord.Interaction, nummer: int):
    # Verbind met SQLite database
    conn = sqlite3.connect("faq.db")
    cursor = conn.cursor()

    # Haal het antwoord op voor de meegegeven vraag-ID
    cursor.execute("SELECT antwoord FROM faq WHERE id = ?", (nummer,))
    row = cursor.fetchone()
    conn.close()

    # Als het antwoord bestaat, stuur het terug naar de gebruiker
    if row:
        await interaction.response.send_message(f"💬 Antwoord op vraag {nummer}:\n{row[0]}")
    else:
        # Als het ID niet bestaat, geef een foutmelding
        await interaction.response.send_message(f"❌ Geen antwoord gevonden voor vraag {nummer}.")

    
    
    
    
    
# Start de bot
bot.run("MTM2MTk3NDAzNjQyMjIwMTM4NA.GVvq-F.C22fIfMfMyFyiv3FTNQzZAAUeR_bj43idbibPw")  # Vergeet je token niet in te vullen!



#oudere versie('s)
""" # Nieuw weercommando
@bot.tree.command(name="weer", description="Haalt de actuele weersomstandigheden op van je weerstation")
async def weer(interaction: discord.Interaction):
    # URL van je weerstation API, vervang deze met de daadwerkelijke URL
    url = "http://145.48.6.82:1337/last/bin"
    
    try:
        # Haal de gegevens op van het weerstation
        response = requests.get(url)
        
        # Controleer of de aanvraag succesvol was
        if response.status_code == 200:
            # Verwerk de ontvangen data (de structuur van je API kan anders zijn)
            data = response.json()
            
            # Verwerk de data (deze zijn slechts voorbeeldnamen, pas aan naar de daadwerkelijke data die je ontvangt)
            temperatuur = data.get('temperature', 'Onbekend')
            luchtvochtigheid = data.get('humidity', 'Onbekend')
            wind_snelheid = data.get('windspeed', 'Onbekend')
            zonnestraling = data.get('solar_radiation', 'Onbekend')
            
            # Verstuur de weerinformatie naar Discord
            await interaction.response.send_message(
                f"🌤 **Actueel Weer** 🌤\n"
                f"Temperatuur: {temperatuur}°C\n"
                f"Luchtvochtigheid: {luchtvochtigheid}%\n"
                f"Wind Snelheid: {wind_snelheid} km/h\n"
                f"Zonnestraling: {zonnestraling} W/m²"
            )
        else:
            await interaction.response.send_message("❌ Fout bij het ophalen van weergegevens.")
    
    except Exception as e:
        await interaction.response.send_message(f"❌ Er is een fout opgetreden: {str(e)}")
    """