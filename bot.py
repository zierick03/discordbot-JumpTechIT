#aan GITHUB gekoppeld test 6
#aan argoCD gekoppeld test 1
#argocdtest 7

# Vereiste packages installeren:
# pip install discord.py mysql-connector-python
#pip install psutil
#C:\Python312\python.exe -m pip install -U discord.py
#C:\Python312\python.exe -m pip install mysql-connector-python
#C:\Python312\python.exe -m pip install psutil



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
#/poll vraag:Wat wil je eten? opties:Pizza,Sushi,Burger
#/rpg rock papaer
#/
#/
#/coins 
#/daily
#/dashboard
#/updates
#/event
#/onderhoud
#/avater

#alleen mogelijk  op server waar bot op draait
# /systemscan         – Haalt systeeminformatie op via het 'systeminfo'-commando (Windows-only)
# /myip               – Toont het externe IP-adres van de machine waarop de bot draait
# /traceroute <host>  – Voert een traceroute uit naar de opgegeven host (platform-afhankelijk)


import discord
import random
import socket  # Voor DNS-resolutie en wake up lan 
import urllib.request  # Voor IP-opvraag
import mysql.connector
from discord.ext import commands
from discord import app_commands
import subprocess
from discord.ext import tasks
import psutil
import datetime
import asyncio

import re #voor wakeup lan 


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

#als je hem opstart dashboard
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


# Kanaal-ID waar dashboard gepost wordt aankondigings kanaalen (updates) bij elke minuut 
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

       
#handmatig dashboard   
@bot.tree.command(name="dashboard", description="Toon het huidige serververbruik (CPU, RAM, opslag)")
async def dashboard(interactie: discord.Interaction):
    await interactie.response.defer(thinking=True)

    stats = get_system_stats()  # Gebruik je bestaande functie
    embed = discord.Embed(title="📊 Serververbruik", description=stats, color=discord.Color.blurple())
    embed.timestamp = datetime.datetime.now()

    await interactie.followup.send(embed=embed)
       
            
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

    
#steen papier schaar /rps
@bot.tree.command(name="rps", description="Speel steen/papier/schaar")
@app_commands.describe(keuze="Kies steen, papier of schaar")
async def rps(interaction: discord.Interaction, keuze: str):
    keuzes = ["steen", "papier", "schaar"]
    keuze = keuze.lower()
    if keuze not in keuzes:
        await interaction.response.send_message("❌ Kies steen, papier of schaar", ephemeral=True)
        return

    bot_keuze = random.choice(keuzes)
    resultaat = "Gelijkspel!"
    if (
        (keuze == "steen" and bot_keuze == "schaar") or
        (keuze == "papier" and bot_keuze == "steen") or
        (keuze == "schaar" and bot_keuze == "papier")
    ):
        resultaat = "Jij wint!"
    elif keuze != bot_keuze:
        resultaat = "Bot wint!"

    await interaction.response.send_message(f"👤 {keuze} vs 🤖 {bot_keuze} → **{resultaat}**")
    

        
        
#xp systeem /daily
user_data = {}
cooldowns = {}

@bot.tree.command(name="daily", description="Claim je dagelijkse reward")
async def daily(interaction: discord.Interaction):
    user = interaction.user.id
    now = datetime.datetime.utcnow()

    if user in cooldowns:
        diff = now - cooldowns[user]
        if diff.total_seconds() < 86400:
            await interaction.response.send_message("⏳ Je hebt al je daily reward geclaimd vandaag!", ephemeral=True)
            return

    cooldowns[user] = now
    # Voeg XP of coins toe in een database
    await interaction.response.send_message("🎁 Je hebt 100 coins ontvangen!")
    
    
    #HAALT DE PROFIELFOTO VAN LEDEN OP 
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Ingelogd als {bot.user}")
    #HOORT BIJ ELKAAR
@bot.tree.command(name="avatar", description="Bekijk de profielfoto van een gebruiker.")
@app_commands.describe(lid="De gebruiker waarvan je de avatar wilt zien")
async def avatar(interaction: discord.Interaction, lid: discord.Member = None):
    lid = lid or interaction.user
    embed = discord.Embed(
        title=f"🖼️ Avatar van {lid.display_name}",
        color=discord.Color.blue()
    )
    embed.set_image(url=lid.display_avatar.url)
    await interaction.response.send_message(embed=embed)







#werkt nog niet optimaal

    #zegt nog steeds 0 hij slaat hem of niet goed op of hij hjaalt hem verkeerdt op 
    
#coins aantal zien  /coins
@bot.tree.command(name="coins", description="Bekijk hoeveel coins je hebt")
async def coins(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    #waarom staat er hier een null/0
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    coins = user_data.get(user_id, 0)
    
    await interaction.response.send_message(
        f"💸 {interaction.user.mention}, je hebt momenteel **{coins} coins**!",
        ephemeral=False
    )

#staat op utc == amsterdam -2 uur kijken of ik dat kan aanpassen 
    
#add event /addevent    


EVENT_CHANNEL_ID = 1380125889475645521  # Vul dit in met je eigen kanaal-ID
events = []

@bot.tree.command(name="addevent", description="Voeg een event toe met herinnering")
@app_commands.describe(naam="Naam van het event", tijd="DD-MM-YYYY HH:MM (UTC)")
async def addevent(interaction: discord.Interaction, naam: str, tijd: str):
    try:
        tijd_dt = datetime.datetime.strptime(tijd, "%d-%m-%Y %H:%M")
    except ValueError:
        await interaction.response.send_message("❌ Tijdformaat moet zijn: DD-MM-YYYY HH:MM", ephemeral=True)
        return

    async def wait_and_send(seconds, message):
        wait_time = (tijd_dt - datetime.datetime.utcnow()).total_seconds() - seconds
        if wait_time > 0:
            await asyncio.sleep(wait_time)
            await channel.send(message)

    # Event opslaan
    events.append((interaction.user.id, naam, tijd_dt))
    await interaction.response.send_message(f"📅 Event '{naam}' aangemaakt voor {tijd_dt} UTC")

    #haaalt het channel op waar hij word versuutr 
    channel = bot.get_channel(EVENT_CHANNEL_ID)

    # Herinnering 1 uur van tevoren
    # await asyncio.sleep((tijd_dt - datetime.datetime.utcnow()).total_seconds() - 3600)
    # if channel:
    #     await channel.send(f"🔔 Herinnering: Event '**{naam}**' begint over 1 uur! (aangemaakt door {interaction.user.mention})")

    # Aanmaakmelding (direct)
    await channel.send(f"📝 Event '**{naam}**' is aangemaakt door {interaction.user.mention} en gepland op {tijd_dt} UTC.")

    # 1 maand (~30 dagen) van tevoren
    await wait_and_send(3600*24*30, f"🔔 Herinnering: Event '**{naam}**' begint over 1 maand! (aangemaakt door {interaction.user.mention})")

    # 1 week van tevoren
    await wait_and_send(3600*24*7, f"🔔 Herinnering: Event '**{naam}**' begint over 1 week! (aangemaakt door {interaction.user.mention})")

    # 1 dag van tevoren
    await wait_and_send(3600*24, f"🔔 Herinnering: Event '**{naam}**' begint over 1 dag! (aangemaakt door {interaction.user.mention})")

    # 5 uur van tevoren
    await wait_and_send(3600*5, f"🔔 Herinnering: Event '**{naam}**' begint over 5 uur! (aangemaakt door {interaction.user.mention})")

    # 1 uur van tevoren
    await wait_and_send(3600, f"🔔 Herinnering: Event '**{naam}**' begint over 1 uur! (aangemaakt door {interaction.user.mention})")
  
        
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





#########################################################wake on lan#########################################################


# voor als je iedereen zelf zijn mac moet invoeren


# # --- Hulpfunctie Wake-on-LAN ---
# def send_wol(mac: str):
#     """
#     Stuurt een Wake-on-LAN (WOL) magic packet.
#     - mac: MAC-adres van de server, bv. "AA:BB:CC:DD:EE:FF"
#     Werkt alleen als de bot in hetzelfde LAN zit als de server.
#     """
#     # MAC-adres schoonmaken (alleen hex-tekens)
#     mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac)
#     if len(mac_clean) != 12:
#         raise ValueError("Ongeldig MAC-adres. Voorbeeld: AA:BB:CC:DD:EE:FF")
    
#     # Magic packet samenstellen: 6x 0xFF + 16x MAC
#     mac_bytes = bytes.fromhex(mac_clean)
#     packet = b'\xff' * 6 + mac_bytes * 16

#     # UDP socket voor broadcast
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#         s.sendto(packet, ("255.255.255.255", 9))  # Standaard WOL-poort is 9

# # --- Slash-command voor WOL ---
# @bot.tree.command(name="wake", description="Weet een server in je LAN wakker")
# @app_commands.describe(mac="MAC-adres van de server (AA:BB:CC:DD:EE:FF)")
# async def slash_wake(interaction: discord.Interaction, mac: str):
#     """
#     - Gebruiker typt /wake <MAC>
#     - Bot verstuurt magic packet naar server
#     """
#     await interaction.response.defer(thinking=True)
#     try:
#         send_wol(mac)
#         await interaction.followup.send(f"✅ Magic packet verzonden naar `{mac}`", ephemeral=True)
#     except Exception as e:
#         await interaction.followup.send(f"❌ Kon WOL niet versturen: `{e}`", ephemeral=True)

# # --- Optioneel: prefix-command !wake ---
# @bot.command(name="wake")
# async def wake_cmd(ctx, mac: str):
#     """
#     Zelfde als slash-command, maar via !wake <MAC>
#     """
#     try:
#         send_wol(mac)
#         await ctx.send(f"✅ Magic packet verzonden naar `{mac}`")
#     except Exception as e:
#         await ctx.send(f"❌ Kon WOL niet versturen: `{e}`")


#########################################################wake on lan#########################################################



# --- Stel je server-MAC hier in ---
SERVER_MAC = "90-FB-A6-80-08-C4"

# --- Zet dit op True op de machine die WOL mag sturen ---
IS_MASTER = True  # Zet op False op andere plekken

# --- Hulpfunctie Wake-on-LAN ---
def send_wol(mac: str):
    """
    Stuurt een Wake-on-LAN (WOL) magic packet.
    Werkt alleen binnen hetzelfde LAN.
    """
    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac)
    if len(mac_clean) != 12:
        raise ValueError("Ongeldig MAC-adres. Voorbeeld: AA:BB:CC:DD:EE:FF")
    
    mac_bytes = bytes.fromhex(mac_clean)
    packet = b'\xff' * 6 + mac_bytes * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(packet, ("255.255.255.255", 9))

# --- Slash-command voor WOL ---
@bot.tree.command(name="wake", description="Weet de server wakker")
async def slash_wake(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    if not IS_MASTER:
        await interaction.followup.send(
            "❌ Deze bot is geen master en mag de server niet wakker maken.",
            ephemeral=True
        )
        return
    try:
        send_wol(SERVER_MAC)
        await interaction.followup.send(
            f"✅ Magic packet verzonden naar server `{SERVER_MAC}`",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Kon WOL niet versturen: `{e}`", ephemeral=True)

# --- Prefix-command !wake ---
@bot.command(name="wake")
async def wake_cmd(ctx):
    if not IS_MASTER:
        await ctx.send("❌ Deze bot is geen master en mag de server niet wakker maken.")
        return
    try:
        send_wol(SERVER_MAC)
        await ctx.send(f"✅ Magic packet verzonden naar server `{SERVER_MAC}`")
    except Exception as e:
        await ctx.send(f"❌ Kon WOL niet versturen: `{e}`")


################wake on lan einde######################### 

# Start de bot
bot.run("MTM2MTk3NDAzNjQyMjIwMTM4NA.GVvq-F.C22fIfMfMyFyiv3FTNQzZAAUeR_bj43idbibPw")  # Vergeet je token niet te beveiligen!