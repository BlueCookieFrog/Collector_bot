import discord
from discord.ext import commands
import json
import aiohttp
import aiofiles
from datetime import datetime as dt


class Exams(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot

    @commands.command(hidden=True)
    async def test(self, ctx, option, *, reactions=None):
        """
        Zapisuje reakcje jakie będą dodawane podczas testu
        Usage
        ----------
        test (option) (reactions)

        Parameters
        ----------
        option :
            backup  - Zapis wysyłanych plików,
            delete  - Usunięcie instniejącego testu,
        WIP check   - Sprawdzenie obecnych ustawien;
        reactions : string
            Reakcje, które bot będzie dodawał do wiadomości;
        """

        """
        TODO:
        *dodać możliwość wyłączania trybu testu, oraz go wznawiania bez potrzeby usuwania i dodawania go na nowo
        *add option to pause/resume test mode without need to delete and set it up again
        """
        try:
            # try to open file and load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)
        except IOError:
            # if file does not exist create it
            with open("config/exams.json", "w+") as f:
                t = {}
                json.dump(t, f, indent=4)
            # load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)

        if option == "delete":
            try:
                # try delete record
                data[str(ctx.guild.id)].pop(str(ctx.channel.id))
                # delete server record if it is empty
                if not bool(data[str(ctx.guild.id)]):
                    data.pop(str(ctx.guild.id))
            except KeyError:
                await ctx.send(
                    "Kanał nie posiada ustawionego testu lub wystąpił nieoczekiwany błąd"
                )
        elif option == "check":
            try:
                await ctx.send(
                    f"Kanał posiada ustawiony test z obecnym ustawieniem:\n- option: {data[str(ctx.guild.id)][str(ctx.channel.id)]['option']} \n- reactions: {data[str(ctx.guild.id)][str(ctx.channel.id)]['reactions']}"
                )
            except KeyError:
                pass
        else:
            # if command is not set to delete record then proceed with setting up test

            # temporary dictionary with channel settings
            temp_dict = {"reactions": reactions.split(), "option": option}

            try:
                # update settings if record exists for current channel
                data[str(ctx.guild.id)][str(ctx.channel.id)].update(temp_dict)
            except KeyError:
                try:
                    # add channel if there is record for server but not for channel
                    data[str(ctx.guild.id)][str(ctx.channel.id)] = temp_dict
                except KeyError:
                    # add record if there is non for neither channel nor server
                    data[str(ctx.guild.id)] = {f"{str(ctx.channel.id)}": temp_dict}

        with open("./config/exams.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.command(hidden=True)
    async def send(self, ctx):
        try:
            # try to open file and load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)
        except IOError:
            print("IOError")

        await ctx.send(data[str(ctx.guild.id)][str(ctx.channel.id)]["reactions"])


class MUD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mud(self, ctx, type):

        if int(type) == (1 or 8 or 20):
            att = len(ctx.message.attachments)
            if att > 0:
                for x in range(att):

                    try:
                        async with aiohttp.ClientSession() as session:

                            # file url
                            url = ctx.message.attachments[x].url

                            # file name
                            name = ctx.message.attachments[x].filename[:-4]

                            # file format
                            file_format = ctx.message.attachments[x].filename[-4:]

                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    """ Adds timestamp to file name to prevent overwriting files with same name"""
                                    now = dt.now()
                                    dt_string = now.strftime("%d%m%Y%H%M%S%f")
                                    f = await aiofiles.open(
                                        f"files/MUD/{name}_{dt_string}{file_format}",
                                        mode="wb",
                                    )
                                    await f.write(await resp.read())
                                    await f.close()

                        await ctx.message.add_reaction(emoji="🇦")
                        await ctx.message.add_reaction(emoji="🇧")
                        await ctx.message.add_reaction(emoji="🇨")
                        await ctx.message.add_reaction(emoji="🇩")
                        await ctx.message.add_reaction(emoji="🇪")
                        await ctx.message.add_reaction(emoji="🇫")
                    except:
                        channel = ctx.message.channel
                        await channel.send("Unexpected error", delete_after=10)

        elif int(type) == 2:
            att = len(ctx.message.attachments)
            if att > 0:
                for x in range(att):

                    try:
                        async with aiohttp.ClientSession() as session:

                            # file url
                            url = ctx.message.attachments[x].url

                            # file name
                            name = ctx.message.attachments[x].filename[:-4]

                            # file format
                            file_format = ctx.message.attachments[x].filename[-4:]

                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    """ Adds timestamp to file name to prevent overwriting files with same name"""
                                    now = dt.now()
                                    dt_string = now.strftime("%d%m%Y%H%M%S%f")
                                    f = await aiofiles.open(
                                        f"files/MUD/{name}_{dt_string}{file_format}",
                                        mode="wb",
                                    )
                                    await f.write(await resp.read())
                                    await f.close()
                        await ctx.message.add_reaction(emoji="1️⃣")
                        await ctx.message.add_reaction(emoji="✔")
                        await ctx.message.add_reaction(emoji="❌")
                        await ctx.message.add_reaction(emoji="2️⃣")
                        await ctx.message.add_reaction(emoji="✅")
                        await ctx.message.add_reaction(emoji="✖")
                        await ctx.message.add_reaction(emoji="3️⃣")
                        await ctx.message.add_reaction(emoji="🟢")
                        await ctx.message.add_reaction(emoji="🔴")
                        await ctx.message.add_reaction(emoji="4️⃣")
                        await ctx.message.add_reaction(emoji="🟩")
                        await ctx.message.add_reaction(emoji="🟥")
                        await ctx.message.add_reaction(emoji="5️⃣")
                        await ctx.message.add_reaction(emoji="💚")
                        await ctx.message.add_reaction(emoji="❤")
                        await ctx.message.add_reaction(emoji="6️⃣")
                        await ctx.message.add_reaction(emoji="🈯")
                        await ctx.message.add_reaction(emoji="🅾")
                    except:
                        channel = ctx.message.channel
                        await channel.send("Unexpected error", delete_after=10)

        elif int(type) == 13:
            att = len(ctx.message.attachments)
            if att > 0:
                for x in range(att):

                    try:
                        async with aiohttp.ClientSession() as session:

                            # file url
                            url = ctx.message.attachments[x].url

                            # file name
                            name = ctx.message.attachments[x].filename[:-4]

                            # file format
                            file_format = ctx.message.attachments[x].filename[-4:]

                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    """ Adds timestamp to file name to prevent overwriting files with same name"""
                                    now = dt.now()
                                    dt_string = now.strftime("%d%m%Y%H%M%S%f")
                                    f = await aiofiles.open(
                                        f"files/MUD/{name}_{dt_string}{file_format}",
                                        mode="wb",
                                    )
                                    await f.write(await resp.read())
                                    await f.close()

                        await ctx.message.add_reaction(emoji="✅")
                        await ctx.message.add_reaction(emoji="❌")
                    except:
                        channel = ctx.message.channel
                        await channel.send("Unexpected error", delete_after=10)

        elif int(type) == 15:
            att = len(ctx.message.attachments)
            if att > 0:
                for x in range(att):

                    try:
                        async with aiohttp.ClientSession() as session:

                            # file url
                            url = ctx.message.attachments[x].url

                            # file name
                            name = ctx.message.attachments[x].filename[:-4]

                            # file format
                            file_format = ctx.message.attachments[x].filename[-4:]

                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    """ Adds timestamp to file name to prevent overwriting files with same name"""
                                    now = dt.now()
                                    dt_string = now.strftime("%d%m%Y%H%M%S%f")
                                    f = await aiofiles.open(
                                        f"files/MUD/{name}_{dt_string}{file_format}",
                                        mode="wb",
                                    )
                                    await f.write(await resp.read())
                                    await f.close()

                    except:
                        channel = ctx.message.channel
                        await channel.send("Unexpected error", delete_after=10)

        elif int(type) == 21:
            att = len(ctx.message.attachments)
            if att > 0:
                for x in range(att):

                    try:
                        async with aiohttp.ClientSession() as session:

                            # file url
                            url = ctx.message.attachments[x].url

                            # file name
                            name = ctx.message.attachments[x].filename[:-4]

                            # file format
                            file_format = ctx.message.attachments[x].filename[-4:]

                            async with session.get(url) as resp:
                                if resp.status == 200:
                                    """ Adds timestamp to file name to prevent overwriting files with same name"""
                                    now = dt.now()
                                    dt_string = now.strftime("%d%m%Y%H%M%S%f")
                                    f = await aiofiles.open(
                                        f"files/MUD/{name}_{dt_string}{file_format}",
                                        mode="wb",
                                    )
                                    await f.write(await resp.read())
                                    await f.close()

                    except:
                        channel = ctx.message.channel
                        await channel.send("Unexpected error", delete_after=10)
        else:
            pass


def setup(bot):
    bot.add_cog(Exams(bot))
    bot.add_cog(MUD(bot))
