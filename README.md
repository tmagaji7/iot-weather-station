# IoT Weather Station with Raspberry Pi & ThingSpeak 

This project uses a Raspberry Pi and DHT11 sensor to build a real-time IoT-based weather monitoring system. Sensor data is uploaded to the ThingSpeak cloud for visualization and analytics, with Twitter and email alerts based on conditions.

## Features
- Real-time temperature & humidity monitoring
- Cloud data analytics using ThingSpeak REST API
- Local data logging and web interface (Flask)
- Twitter and email alert integration
- Auto start on Raspberry Pi boot

## Setup Instructions
1. Connect DHT11 to GPIO 21
2. Create a ThingSpeak account and get the API key
3. Configure `.env` file with keys
4. Run `pip install -r requirements.txt`
5. Run `python3 main.py`



