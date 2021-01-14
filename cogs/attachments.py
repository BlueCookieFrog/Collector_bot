import discord
import json
from discord.ext import commands
import aiohttp
import aiofiles
import os
from datetime import datetime as dt


class Attachments(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # print(message.channel.id)

        """
        Part that, for now, downloads file that is attached to message and saves it in /files directory

        TODO:
        - GDrive integration
        """
        att = len(message.attachments)
        if att > 0:
            for x in range(att):

                if str(message.channel) == "na-puste-pytania":
                    await message.add_reaction(emoji="✔️")
                    await message.add_reaction(emoji="❌")
                    await message.add_reaction(emoji="⏭️")

                    try:
                        async with aiohttp.ClientSession() as session:

                            # file url
                            url = message.attachments[x].url

                            # file name
                            name = message.attachments[x].filename[:-4]

                            # file format
                            file_format = message.attachments[x].filename[-4:]

                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    """ Adds timestamp to file name to prevent overwriting files with same name"""
                                    now = dt.now()
                                    dt_string = now.strftime("%d%m%Y%H%M%S%f")
                                    f = await aiofiles.open(
                                        f"files/Air2k18/{name}_{dt_string}{file_format}",
                                        mode="wb",
                                    )
                                    await f.write(await resp.read())
                                    await f.close()

                    except:
                        channel = message.channel
                        await channel.send("Unexpected error", delete_after=10)

                if str(message.channel) == "kolokwium-02-12":
                    await message.add_reaction(emoji="🇦")
                    await message.add_reaction(emoji="🇧")
                    await message.add_reaction(emoji="🇨")
                    await message.add_reaction(emoji="🇩")
                    await message.add_reaction(emoji="🇪")
                    await message.add_reaction(emoji="🇫")

                    try:
                        async with aiohttp.ClientSession() as session:

                            # file url
                            url = message.attachments[x].url

                            # file name
                            name = message.attachments[x].filename[:-4]

                            # file format
                            file_format = message.attachments[x].filename[-4:]

                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    """ Adds timestamp to file name to prevent overwriting files with same name"""
                                    now = dt.now()
                                    dt_string = now.strftime("%d%m%Y%H%M%S%f")
                                    f = await aiofiles.open(
                                        f"files/Brzeski/{name}_{dt_string}{file_format}",
                                        mode="wb",
                                    )
                                    await f.write(await resp.read())
                                    await f.close()
                    except:
                        channel = message.channel
                        await channel.send("Unexpected error", delete_after=10)

        """ If message only consist of bot mention, bot will reply with current prefix """

        if str(message.content)[3:-1] == str(self.bot.user.id) and str(
            message.author
        ) != str(self.bot.user):
            with open("./config/prefixes.json", "r") as f:
                prefixes = json.load(f)

            channel = message.channel
            await channel.send(f"Current prefix: {prefixes[str(message.guild.id)]}")


def setup(bot):
    bot.add_cog(Attachments(bot))
