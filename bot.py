# Vereiste packages installeren:
# pip install discord.py mysql-connector-python


#aanmaken database




import discord
import random
import mysql.connector
from discord.ext import commands

# MySQL-verbinding
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # Pas aan als nodig niet veilig dat weet ik 
        password="P@ssword",    # Pas aan als nodig niet veilig dat weet ik 
        database="discordbot"
    )

# Bot setup met intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=["/", "!"], intents=intents)

# Event: Bot is online
@bot.event
async def on_ready():
    print(f'✅ Bot is online als: {bot.user}')
    await bot.tree.sync()  # Slash-commands synchroniseren
    print("✅ Slash-commando's zijn gesynchroniseerd!")

# Normale prefix-commando's
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
    getal = random.randint(start, einde)
    await ctx.send(f'Het willekeurige getal tussen {start} en {einde} is: {getal}')

# Slash-commando's
@bot.tree.command(name="hoi", description="Zegt hoi tegen de gebruiker")
async def slash_hoi(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hoi {interaction.user.mention}! 👋')

@bot.tree.command(name="hallo", description="Groet de gebruiker")
async def slash_hallo(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hallo {interaction.user.mention}, hoe gaat het? 😄')

@bot.tree.command(name="ping", description="Test de bot latency")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.tree.command(name="randomgetal", description="Geef een willekeurig getal tussen start en einde")
async def slash_randomgetal(interaction: discord.Interaction, start: int, einde: int):
    getal = random.randint(start, einde)
    await interaction.response.send_message(f'Het willekeurige getal tussen {start} en {einde} is: {getal}')

# Slash-commando voor contact
@bot.tree.command(name="contact", description="Geef contactinformatie")
async def contact(interaction: discord.Interaction):
    contact_info = """
📧 E-mail: zierick@jumptechit.nl  
📱 Telefoon: 06-38273136  
📷 Instagram: JumpTechIT  
🔗 LinkedIn: Jumptech-it
    """
    await interaction.response.send_message(contact_info)

# Slash-commando voor FAQ-lijst
@bot.tree.command(name="faq", description="Toon een lijst met veelgestelde vragen")
async def faq(interaction: discord.Interaction):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, vraag FROM faq")
    vragen = cursor.fetchall()
    conn.close()

    if not vragen:
        await interaction.response.send_message("❌ Geen vragen gevonden.")
        return

    antwoord = "**📋 Veelgestelde Vragen:**\n"
    for id, vraag in vragen:
        antwoord += f"{id}. {vraag}\n"
    antwoord += "\nGebruik `/faq_antwoord <nummer>` om het antwoord te zien."
    await interaction.response.send_message(antwoord)

# Slash-commando om antwoord op 1 specifieke vraag op te halen
@bot.tree.command(name="faq_antwoord", description="Geef antwoord op een specifieke FAQ-vraag")
async def faq_antwoord(interaction: discord.Interaction, nummer: int):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT antwoord FROM faq WHERE id = %s", (nummer,))
    result = cursor.fetchone()
    conn.close()

    if result:
        await interaction.response.send_message(f"💬 Antwoord op vraag {nummer}:\n{result[0]}")
    else:
        await interaction.response.send_message("❌ Geen antwoord gevonden voor vraag {nummer}.")

# Start de bot
bot.run("MTM2MTk3NDAzNjQyMjIwMTM4NA.GVvq-F.C22fIfMfMyFyiv3FTNQzZAAUeR_bj43idbibPw")  # Vergeet je token niet te beveiligen!


#EEN KEER RUNNEN IN EEN APART *.DB BESTAND OM DATABASE AAN TE MAKEN 
# CREATE DATABASE IF NOT EXISTS discordbot;
# USE discordbot;

# CREATE TABLE IF NOT EXISTS faq (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     vraag TEXT NOT NULL,
#     antwoord TEXT NOT NULL
# );

# INSERT INTO faq (vraag, antwoord) VALUES
# ('Wat zijn jullie openingstijden?', 'We zijn geopend van maandag t/m vrijdag van 09:00 tot 17:00.'),
# ('Hoe neem ik contact op?', 'Mail naar info@example.com of bel 0123-456789.'),
# ('Waar is jullie kantoor?', 'Hoofdstraat 123, Eindhoven.'),
# ('Bieden jullie support?', 'Ja, via mail en telefoon.'),
# ('Hoe maak ik een afspraak?', 'Via onze website of telefonisch.'),
# ('Nieuwsbrief?', 'Ja, aanmelden via de website.'),
# ('Betaalmogelijkheden?', 'iDEAL, PayPal en creditcard.'),
# ('Retourneren?', 'Binnen 14 dagen mits ongebruikt.'),
# ('Duurzaam?', 'Ja, we richten ons op duurzaamheid.'),
# ('Werken jullie op locatie?', 'Ja, op afstand en locatie.');

