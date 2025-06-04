# Vereiste packages installeren:
# pip install discord.py mysql-connector-python
#pip install psutil



#aanmaken database

# ✅ Slash-commando overzicht:

# /hoi                – Zegt hoi tegen de gebruiker
# /hallo              – Groet de gebruiker vriendelijk
# /ping               – Test de latency van de bot
# /randomgetal        – Genereert een willekeurig getal tussen opgegeven grenzen
# /contact            – Toont contactinformatie van JumpTechIT
# /faq                – Toont een lijst met veelgestelde vragen uit de database
# /faq_antwoord       – Geeft antwoord op een specifieke veelgestelde vraag
#/update titel:Belangrijke Update inhoud:De nieuwe feature is live vanaf maandag!


#alleen mogelijk  op server waar bot op draait
# /systemscan         – Haalt systeeminformatie op via het 'systeminfo'-commando (Windows-only)
# /myip               – Toont het externe IP-adres van de machine waarop de bot draait
# /traceroute <host>  – Voert een traceroute uit naar de opgegeven host (platform-afhankelijk)

#nog niet werkend 
#/poll vraag:Wat wil je eten? opties:Pizza,Sushi,Burger


#automatische 
#ieder minuur server update 

import discord
import random
import socket  # Voor DNS-resolutie
import urllib.request  # Voor IP-opvraag
import mysql.connector
from discord.ext import commands
from discord import app_commands
import subprocess
from discord.ext import tasks
import psutil
import datetime






# Kanaal-ID waar dashboard gepost wordt
DASHBOARD_CHANNEL_ID = 1379833746701684776  # Vervang door jouw kanaal-ID


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
    
@bot.command()
async def myip(ctx):
    """Geeft het externe IP-adres van de machine waarop de bot draait."""
    try:
        ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        await ctx.send(f"🌐 Extern IP-adres: `{ip}`")
    except Exception as e:
        await ctx.send(f"❌ Fout bij ophalen van IP-adres:\n```{str(e)}```")

@bot.command()
async def traceroute(ctx, host: str):
    """Voert een traceroute uit naar een opgegeven host (bv. google.com)."""
    try:
        # Gebruik platform-afhankelijke commando’s
        import platform
        if platform.system() == "Windows":
            cmd = f"tracert {host}"
        else:
            cmd = f"traceroute {host}"
        
        resultaat = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        # Splits output op in Discord-vriendelijke blokken
        MAX_DISCORD_LENGTH = 1900
        for i in range(0, len(resultaat), MAX_DISCORD_LENGTH):
            await ctx.send(f"```{resultaat[i:i+MAX_DISCORD_LENGTH]}```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"❌ Fout tijdens traceroute:\n```{e.output}```")
    except Exception as e:
        await ctx.send(f"❌ Onbekende fout:\n```{str(e)}```")
        
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

#haalt al je PC gebruik op werkt alleen als de bot op jouw PC draait /systeminfo 
@bot.command()
async def systemscan(ctx):
    """Haalt basis systeeminformatie op via systeminfo (alleen Windows)."""
    try:
        # Voer 'systeminfo' uit via subprocess
        resultaat = subprocess.check_output("systeminfo", shell=True, text=True, stderr=subprocess.STDOUT)
        # Discord heeft limieten, splits resultaat op in stukken van max 1900 tekens
        MAX_DISCORD_LENGTH = 1900
        for i in range(0, len(resultaat), MAX_DISCORD_LENGTH):
            await ctx.send(f"```{resultaat[i:i+MAX_DISCORD_LENGTH]}```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"❌ Fout bij ophalen van systeeminfo:\n```{e.output}```")
    except Exception as e:
        await ctx.send(f"❌ Onbekende fout:\n```{str(e)}```")




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


#nieuwsupdates invoegen  /updates
@bot.tree.command(name="update", description="Post een nieuwsupdate of aankondiging")
async def update(interaction: discord.Interaction, titel: str, inhoud: str):
    embed = discord.Embed(
        title=f"📢 {titel}",
        description=inhoud,
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Gepost door: {interaction.user.display_name}")
    embed.timestamp = interaction.created_at

    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Aankondiging geplaatst!", ephemeral=True)



#onderhoud invoegen  /onderhoud
@bot.tree.command(name="onderhoud", description="Post een onderhoud of aankondiging")
async def update(interaction: discord.Interaction, titel: str, inhoud: str):
    embed = discord.Embed(
        title=f"🔧 {titel}",
        description=inhoud,
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Gepost door: {interaction.user.display_name}")
    embed.timestamp = interaction.created_at

    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Aankondiging geplaatst!", ephemeral=True)



# Functie die het dashboard update (zonder loop)

# # Slash command om het dashboard handmatig te updaten
# @bot.tree.command(name="update_dashboard", description="Update het dashboard handmatig")
# async def update_dashboard_command(interaction: discord.Interaction):
#     await send_or_update_dashboard()
#     await interaction.response.send_message("✅ Dashboard is bijgewerkt!", ephemeral=True)


#als je hem opstart 
async def send_or_update_dashboard():
    global dashboard_message
    channel = bot.get_channel(1379833746701684776)
    if channel is None:
        print("⚠️ Dashboard kanaal niet gevonden!")
        return

    stats_text = get_system_stats()
    embed = discord.Embed(title="📊 Dashboard", description=stats_text, color=discord.Color.green())
    embed.timestamp = datetime.datetime.now()


    if dashboard_message is None:
        dashboard_message = await channel.send(embed=embed)
    else:
        try:
            await dashboard_message.edit(embed=embed)
        except discord.NotFound:
            dashboard_message = await channel.send(embed=embed)


# Kanaal-ID waar dashboard gepost wordt aankondigings kanaalen (updates)
DASHBOARD_CHANNEL_ID = 1379833746701684776  # Vervang door jouw kanaal-ID

dashboard_message = None  # Dit bewaren we zodat we het bericht kunnen updaten

def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    uptime_seconds = (datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds()
    uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))

    stats = (
        f"**Systeemstatus (Realtime)**\n"
        f"CPU gebruik: {cpu_percent}%\n"
        f"Geheugen gebruik: {mem.percent}% ({mem.used // (1024*1024)} MB gebruikt van {mem.total // (1024*1024)} MB)\n"
        f"Systeem uptime: {uptime_str}\n"
    )
    return stats

#per minuut 
@tasks.loop(minutes=1)
async def update_dashboard():
    global dashboard_message
    channel = bot.get_channel(DASHBOARD_CHANNEL_ID)
    if channel is None:
        print("⚠️ Dashboard kanaal niet gevonden!")
        return

    stats_text = get_system_stats()
    embed = discord.Embed(title="📊 Dashboard", description=stats_text, color=discord.Color.green())
    embed.timestamp = datetime.datetime.now()


    if dashboard_message is None:
        dashboard_message = await channel.send(embed=embed)
    else:
        try:
            await dashboard_message.edit(embed=embed)
        except discord.NotFound:
            # Bericht is verwijderd, stuur een nieuw bericht
            dashboard_message = await channel.send(embed=embed)
            update_dashboard.start()

            
            






#werkt nog niet 


#poll lijsten 


@bot.tree.command(name="poll", description="Maak een poll met 2-10 opties, gescheiden door komma's")
async def poll(interaction: discord.Interaction, vraag: str, opties: str):
    optie_lijst = [opt.strip() for opt in opties.split(",")]
    if len(optie_lijst) < 2 or len(optie_lijst) > 10:
        await interaction.response.send_message(
            "❌ Geef tussen de 2 en 10 opties op, gescheiden door komma's.",
            ephemeral=True
        )
        return

    emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    beschrijving = "\n".join(f"{emoji_list[i]} {opt}" for i, opt in enumerate(optie_lijst))

    embed = discord.Embed(
        title="📊 Poll",
        description=f"**{vraag}**\n\n{beschrijving}",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Gemaakt door: {interaction.user.display_name}")
    embed.timestamp = interaction.created_at

    await interaction.response.send_message(embed=embed)
    bericht = await interaction.original_response()

    for i in range(len(optie_lijst)):
        await bericht.add_reaction(emoji_list[i])

        
  
    #poll werkend krijgen 


# @bot.event
# async def on_ready():
#     await bot.tree.sync()
#     print(f"{bot.user} is online en slash commands zijn gesynchroniseerd.")





            


            
            
            
            
# Event: Bot is online
@bot.event
async def on_ready():
    print(f'✅ Bot is online als: {bot.user}')
    await bot.tree.sync() #slash commando synchroniseren 
    print("✅ Slash-commando's zijn gesynchroniseerd!")


    # Stuur bericht naar een kanaal
    channel = bot.get_channel(1379833746701684776)
    if channel:
        await channel.send("✅ Bot is opnieuw opgestart en klaar om te gebruiken!")
    update_dashboard.start()


# Start de bot
bot.run("MTM2MTk3NDAzNjQyMjIwMTM4NA.GVvq-F.C22fIfMfMyFyiv3FTNQzZAAUeR_bj43idbibPw")  # Vergeet je token niet te beveiligen!