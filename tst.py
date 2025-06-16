from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()
 
host = os.getenv('MQTT_BROKER')

