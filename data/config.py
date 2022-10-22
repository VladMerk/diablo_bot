import os

from dotenv import load_dotenv

load_dotenv()

token = str(os.getenv("token"))
terror_zone_discord_channel = os.getenv('terror_zone_discord_channel')
clone_discord_channel = os.getenv('clone_discord_channel')
