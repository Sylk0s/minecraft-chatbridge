from discord.ext import tasks

import discord
from redis import Redis
import asyncio
import json

configs = json.load(open("bot/configs.json"))

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        self.p = Redis(host=configs["host"], port=configs["port"], password=configs["pass"]).pubsub()
        self.p.subscribe("messages")
        self.channel = self.get_channel(configs["channel"])
        while not self.is_closed():
            message = self.p.get_message()
            if message:
                s=str(message['data'])
                if not s == "1":
                    parsedMessage = s[2:-1]
                    print(parsedMessage)
                    if(parsedMessage[-10:-2] == "the game") or (parsedMessage[33] == '<'):
                        parsedMessageFinal = parsedMessage[32:-2]
                        await self.channel.send(parsedMessageFinal)
            await asyncio.sleep(0.1)

client = MyClient()
client.run(configs["token"])