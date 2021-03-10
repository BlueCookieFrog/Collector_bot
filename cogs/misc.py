import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot

    @commands.command()
    async def kod(self, ctx):
        link = " "
        await ctx.send(f"Kod bota znajdziesz w repozytorium: {link}")

def setup(bot):
    bot.add_cog(Misc(bot))


