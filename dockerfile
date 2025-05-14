# Gebruik Python 3.11.9 als basis image
FROM python:3.11.9-slim

# Zet de werkdirectory binnen de container
WORKDIR /app

# Kopieer de requirements file en installeer de dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de applicatiecode naar de container
COPY . .

# Open de poort waarop de applicatie draait
EXPOSE 5000

# Zorg ervoor dat de app start bij het uitvoeren van de container
CMD ["python", "app.py"]
