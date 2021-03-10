import discord
from discord.ext import commands
import json

class Exams(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, option: str, *, reactions=None):
        """
        Zapisuje reakcje jakie będą dodawane podczas testu
        Usage
        ----------
        test (option) (reactions)

        Parameters
        ----------
        option :
            backup  - Zapis wysyłanych plików,

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
                json.dump({}, f, indent=4)
            # load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)

        # temporary dictionary with channel settings
        temp_dict = {"reactions": reactions.split(), "option": option, "paused": False}

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

    @commands.command()
    async def menage_test(self, ctx, option: str, additional=None):
        """
        Zarządzanie testami
        Usage
        ----------
        test (option) (reactions)

        Parameters
        ----------
        option :
        WIP resume      - wznowienie działania testu na kanale
        WIP pause       - wstrzymanie działania testu na kanale
            delete      - Usunięcie instniejącego testu,
            delete all  - Usunięcie wszystkich testów,
            check       - Sprawdzenie obecnych ustawien na kanale,
            all         - Sprawdzenie wszystkich testów na serwerze
        """
        try:
            # try to open file and load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)
        except IOError:
            # if file does not exist create it
            with open("config/exams.json", "w+") as f:
                json.dump({}, f, indent=4)
            # load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)

        if option == "resume":
            data[str(ctx.guild.id)][str(ctx.channel.id)]["paused"].update(False)

        elif option == "pause":
            data[str(ctx.guild.id)][str(ctx.channel.id)]["paused"].update(True)

        elif option == "delete":
            # delete test from current channel
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
        elif option == "delete" and additional == "all":
            if ctx.message.author.guild_permissions.administrator:
                try:
                    data.pop(str(ctx.guild.id))
                except KeyError:
                    await ctx.send(
                        "Kanał nie posiada ustawionego testu lub wystąpił nieoczekiwany błąd"
                    )
            else:
                await ctx.send(f"Tylko administrator może usunąć wszystkie testy")

        elif option == "check":
            try:
                if data[str(ctx.guild.id)][str(ctx.channel.id)]["paused"]:
                    await ctx.send(
                        f"Kanał posiada wstrzymany test z obecnym ustawieniem:\n- option: {data[str(ctx.guild.id)][str(ctx.channel.id)]['option']} \n- reactions: {data[str(ctx.guild.id)][str(ctx.channel.id)]['reactions']}"
                    )
                else:
                    await ctx.send(
                        f"Kanał posiada działający test z obecnym ustawieniem:\n- option: {data[str(ctx.guild.id)][str(ctx.channel.id)]['option']} \n- reactions: {data[str(ctx.guild.id)][str(ctx.channel.id)]['reactions']}"
                    )
            except KeyError:
                await ctx.send(f"Kanał nie posiada zdefiniowanego testu")

        elif option == "all":
            try:
                await ctx.send(
                    f"Serwer ma ustawione {len(data[str(ctx.guild.id)])} testów:"
                )
                for channel_id in data[str(ctx.guild.id)].keys():
                    channel_name = self.bot.get_channel(int(channel_id)).name
                    emoji = data[str(ctx.guild.id)][str(ctx.channel.id)]["reactions"]
                    paused = data[str(ctx.guild.id)][str(ctx.channel.id)]["paused"]
                    await ctx.send(
                        f"- Kanał '{channel_name}' z reakcjami {emoji}, wstrzymany - {'Tak' if paused else 'Nie'}"
                    )
            except KeyError:
                await ctx.send(
                    "Serwer nie posiada ustawionych testów lub wystąpił nieoczekiwany błąd"
                )

        with open("./config/exams.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def send(self, ctx):
        try:
            # try to open file and load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)
        except IOError:
            print("IOError")

        await ctx.send(data[str(ctx.guild.id)][str(ctx.channel.id)]["reactions"])


def setup(bot):
    bot.add_cog(Exams(bot))
