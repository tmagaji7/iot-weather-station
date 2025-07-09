import Adafruit_DHT as dht
import time
import requests
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib

# Load API keys from .env file
load_dotenv()
THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Sensor configuration
SENSOR = 11  # DHT11
PIN = 21     # GPIO pin


LOG_FILE = "data_log.csv"

# Email alert threshold
TEMP_THRESHOLD = 35

# Setup CSV if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Temperature", "Humidity"])

def send_email_alert(temp):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f"Subject: Temperature Alert!\n\nALERT: Temperature is too high ({temp} °C)."
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
        server.quit()
        print("Email alert sent!")
    except Exception as e:
        print(f"Email failed: {e}")

while True:
    humidity, temperature = dht.read_retry(SENSOR, PIN)

    if humidity is not None and temperature is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Temp: {temperature:.2f} °C, Humidity: {humidity:.2f}%")

        # Save to CSV
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, temperature, humidity])

        # Send to ThingSpeak
        try:
            url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={temperature}&field2={humidity}"
            response = requests.get(url)
            if response.status_code == 200:
                print("Data sent to ThingSpeak")
            else:
                print(f"ThingSpeak error: {response.status_code}")
        except Exception as e:
            print(f"Failed to send data: {e}")

        # Email alert if temp too high
        if temperature > TEMP_THRESHOLD:
            send_email_alert(temperature)
    else:
        print("Sensor read failed.")

    time.sleep(15)  # Respect ThingSpeak rate limit
