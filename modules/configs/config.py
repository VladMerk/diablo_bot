import os
import logging
from dotenv import load_dotenv


load_dotenv()

token = str(os.getenv("token"))
token_d2r = str(os.getenv("token_d2r"))
terror_zone_discord_channel = int(os.getenv('terror_zone_discord_channel'))
clone_discord_channel = int(os.getenv('clone_discord_channel'))
fast_trade_discord_channel = int(os.getenv('fast_trade_discord_channel'))

admin_role = 1036936360063401984
