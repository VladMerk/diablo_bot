from datetime import datetime
import discord
import json
from discord.ext import tasks, commands
from data.config import token, terror_zone_discord_channel, clone_discord_channel, fast_trade_discord_channel
from terror_zone import terror_zone_def
from clone import clone
import logging

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)


class TerrorBot(commands.Bot):
    terror_zone_channel = terror_zone_discord_channel
    clone_channel = clone_discord_channel
    fast_trade_channel = fast_trade_discord_channel
    time_to_delete_messages = 10 # minutes


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.terrot_zone = ''
        self.clone_dict = {}
        self.clone_dict_rw = {}
        self.flag = 0
        self.top_clone_server = {}

        self.region = {1: 'America',  2: 'Europe',   3: 'Asia'}
        self.ladder = {1: 'Ladder',   2: 'NonLadder'}
        self.hc = {1: 'Hardcore', 2: 'Softcore'}


    async def on_message(self, message: discord.message.Message, /) -> None:
        await self.process_commands(message)
        if message.channel.id in [TerrorBot.terror_zone_channel, TerrorBot.clone_channel]:
            await message.publish()


    def read_json(self, key):
        zone = {}
        with open('zone.json') as file:
            zone = json.load(file)
        return zone[key]

    async def setup_hook(self) -> None:
        self.terror_zone.start()
        self.clone.start()
        self.fast_trade_messages.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=30)
    async def terror_zone(self):
        channel = self.get_channel(TerrorBot.terror_zone_channel)

        def run_job():
            now = datetime.now()
            return now.minute in range(1, 5)

        if run_job():
            zone = terror_zone_def()
            if zone != '' and self.terrot_zone != zone or self.terrot_zone == '':
                self.terrot_zone = zone
                zone_json = self.read_json(self.terrot_zone)
                message = f"\n**Terror Zone**: {zone_json['name']['en']} in **{zone_json['act']} Act**\n"
                message += f"**Зона Ужаса**: {zone_json['name']['ru']} в **{zone_json['act']} акте**\n"
                message += f"\n**Иммунитеты**: {zone_json['immunities']['ru']}\n"
                message += f"**Количество пачек с уникальными мобами**: {zone_json['boss_packs']}\n"
                message += f"**Uniques**: {zone_json['super_uniques']}\n"
                message += f"**Количество особых сундуков**: {zone_json['sparkly_chests']}" if zone_json['sparkly_chests'] > 0 else ''
                message += "\nProvided By <https://d2runewizard.com>"

                await channel.send(message)

    @terror_zone.before_loop
    async def before_terror_zone(self):
        await self.wait_until_ready()


    @tasks.loop(seconds=30)
    async def clone(self):
        channel = self.get_channel(TerrorBot.clone_channel)
        logging.debug('Call clone function')
        progress = clone()
        logging.debug('get functions clone()')
        if self.clone_dict_rw != {}:
            for server in progress:
                if self.clone_dict_rw[server]['progres'] != progress[server]['progres']:
                    self.top_clone_server = server
                    self.flag = 1
                    self.clone_dict_rw = progress
                    break
        else:
            self.clone_dict_rw = progress
            await channel.purge()
            await channel.send(self.get_message(prg=progress))

        if self.flag:
            await channel.purge()
            await channel.send(self.get_message(prg=progress))
            self.flag = 0

    @clone.before_loop
    async def befor_clone(self):
        await self.wait_until_ready()

    def get_server(self, prg: dict, servers: list) -> str:
        mess = ''
        for server in servers:
            if int(prg[server]['progres']) > 1:
                mess += f"**[{prg[server]['progres']}/6]** "
            else:
                mess += f"[{prg[server]['progres']}/6] "
            mess += f"{'Ladder' if prg[server]['ladder'] else 'NonLadder'} "
            mess += f"{'Hardcore' if prg[server]['hardcore'] else 'Softcore'} "
            mess += f"{prg[server]['region']} "
            mess += f"<t:{prg[server]['lastUpdate']}:R>\n"
        return mess + '\n'


    def get_message(self, prg: list) -> str:
        message = ''
        if self.flag:
            message += '\nПоследнее изменение:\n'
            message += self.get_server(prg=prg, servers=[prg[self.top_clone_server]['server']])

        message += '***Ladder***\n'
        message += self.get_server(prg=prg, servers=['ladderSoftcoreAsia', 'ladderSoftcoreEurope', 'ladderSoftcoreAmericas'])
        message += self.get_server(prg=prg, servers=['ladderHardcoreAsia', 'ladderHardcoreEurope', 'ladderHardcoreAmericas'])

        message += '***NonLadder***\n'
        message += self.get_server(prg=prg, servers=['nonLadderSoftcoreAsia', 'nonLadderSoftcoreEurope', 'nonLadderSoftcoreAmericas'])
        message += self.get_server(prg=prg, servers=['nonLadderHardcoreAsia', 'nonLadderHardcoreEurope', 'nonLadderHardcoreAmericas'])

        message += f'\nProvided By <https://d2runewizard.com>'

        return message

    @tasks.loop(seconds=60)
    async def fast_trade_messages(self):
        channel = self.get_channel(TerrorBot.fast_trade_channel)
        if messages := [message async for message in channel.history()]:
            for message in messages:
                # print(message.type, message.pinned)
                # logging.info(f"{message.content} - {int(message.created_at.timestamp())}")
                if int(message.created_at.timestamp()) / 60 + TerrorBot.time_to_delete_messages <= datetime.now().timestamp() / 60 and \
                    not message.pinned:
                    await message.delete()

    @fast_trade_messages.before_loop
    async def before_fast_trade_messages(self):
        await self.wait_until_ready()


if __name__ == '__main__':
    client = TerrorBot(command_prefix='!', intents=discord.Intents.all())
    client.run(token)
