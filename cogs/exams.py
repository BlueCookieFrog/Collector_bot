import discord
from discord.ext import commands
import json


class Exams(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, backup, *, reactions = None):
        """
        Parameters
        ----------
        backup : True/False
            Zapis wysyłanych plików
        reactions : string
            Reakcje, które bot będzie dodawał do wiadomości
        """
        if backup == "delete":
            pass

        else:
            try:
                with open("config/exams.json", "w+") as f:
                    data = json.load(f)
            except IOError:
                with open("config/exams.json", "w+") as f:
                    json.dump({}, f, indent=4)
                    data = json.load(f)

            try:
                data[str(ctx.guild.id)].append({"channel_id": str(ctx.channel.id), "reactions": [], "save_atachments": False })
            except KeyError:
                data[str(ctx.guild.id)] = {"channel_name": str(ctx.channel.id), "reactions": reactions, "save_atachments": backup }


def setup(bot):
    bot.add_cog(Exams(bot))
