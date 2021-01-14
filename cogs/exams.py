import discord
from discord.ext import commands
import json


class Exams(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot


def setup(bot):
    bot.add_cog(Exams(bot))
