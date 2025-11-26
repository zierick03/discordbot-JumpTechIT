# Gebruik een officieel Python 3.10 image
FROM python:3.14.0

# Maak een directory voor je app in de container
WORKDIR /bot

# Kopieer requirements.txt en installeer dependencies
COPY requirements.txt /bot/requirements.txt
RUN pip install --no-cache-dir -r /bot/requirements.txt

# Kopieer de volledige applicatie naar de container
COPY . /bot

# Stel de poort in waarop de bot draait (optioneel)
EXPOSE 8080

# Start de bot wanneer de container draait
CMD ["python", "bot.py"]


#..
# # Gebruik een officieel Python 3.11.9 image
# FROM python:3.10.12

# # Maak een directory voor je app in de container
# WORKDIR /bot

# # Kopieer je requirements.txt bestand naar de container
# COPY requirements.txt /bot/requirements.txt

# # Installeer de Python-afhankelijkheden
# RUN pip install --no-cache-dir -r /bot/requirements.txt

# # Kopieer je hele applicatie (inclusief de botcode) naar de container
# COPY . /bot

# # Stel de poort in waarop de bot draait (dit is niet noodzakelijk voor de bot zelf, maar kan nuttig zijn)
# EXPOSE 8080

# # Het commando om de bot uit te voeren
# CMD ["python", "bot.py"]

# RUN pip install --no-cache-dir -r /bot/requirements.txt
# #RUN python bot.py
