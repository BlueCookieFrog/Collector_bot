import discord
from discord.ext import commands
import json

class Exams(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, backup, *, reactions=None):
        """
        Zapisuje reakcje jakie będą dodawane podczas testu
        Usage
        ----------
        test (backup) (reactions)

        Parameters
        ----------
        backup : True/False/delete
            Zapis wysyłanych plików;
        reactions : string
            Reakcje, które bot będzie dodawał do wiadomości;
        """

        """
        TODO:
        *fix true/false settings
        *change 'backup' to other variable name
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

        if backup == "delete":
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
        else:
            # if command is not set to delete record then proceed with setting up test

            # temporary dictionary with channel settings
            temp_dict = {"reactions": reactions.split(), "save_atachments": backup}

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
    async def send(self, ctx):
        try:
            # try to open file and load it
            with open("config/exams.json", "r") as f:
                data = json.load(f)
        except IOError:
            print('IOError')

        await ctx.send(data[str(ctx.guild.id)][str(ctx.channel.id)]["reactions"])
def setup(bot):
    bot.add_cog(Exams(bot))
