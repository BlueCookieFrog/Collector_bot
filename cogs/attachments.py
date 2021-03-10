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
            try:
                # try to open file and load it
                with open("config/exams.json", "r") as f:
                    data = json.load(f)
                for x in range(att):
                    try:
                        if str(message.channel.id) in data[str(message.guild.id)]:

                            for emoji in data[str(message.guild.id)][
                                str(message.channel.id)
                            ]["reactions"]:
                                await message.add_reaction(emoji)

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

                                            # create directory if it doesn't exist
                                            directory = f"files/{str(message.guild.name)}/{str(message.channel.name)}"
                                            if not os.path.exists(directory):
                                                os.makedirs(directory)

                                            async with aiofiles.open(
                                                f"{directory}/{name}_{dt_string}{file_format}",
                                                mode="wb",
                                            ) as f:
                                                await f.write(await resp.read())

                            except Exception as error:
                                # logging errors without flooding terminal
                                now = dt.now()
                                date = now.strftime("%d.%m.%Y[%H:%M:%S]")
                                log_id = now.strftime("%d%m%Y%H%M%S%f")

                                try:
                                    log = open("log.txt", "a")
                                    # error id which is send in message
                                    log.write(f"{log_id}:\n")
                                    # raised exception
                                    log.write(
                                        f"    {date} - {error.__class__} in attachments.py, on_message, file download\n"
                                    )
                                    # server and channel
                                    log.write(
                                        f'    in server "{message.guild.name}" ({message.guild.id}) and channel "{message.channel.name}" ({message.channel.id})\n'
                                    )
                                except Exception as log_error:
                                    print(
                                        f"Occured error while logging raised exception {log_error.__class__}"
                                    )
                                await message.channel.send(
                                    f"Unexpected error, error id: {log_id}"
                                )
                    except KeyError:
                        pass

            except IOError:
                pass

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
