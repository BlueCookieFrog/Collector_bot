import discord
from discord.ext import commands
import json


class Prefixes(commands.Cog):
    def __init__(self, bot: discord):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Adds entry to json file after joining to server.

        Parameters
        ----------
        guild : discord.Guild
        """
        with open("./config/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "."

        with open("./config/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """Removes entry from json file after leaving server.

        Parameters
        ----------
        guild : discord.Guild
        """
        with open("./config/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open("./config/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    @commands.is_owner()
    async def prefix(self, ctx, pref):
        """Changes prefix

        Parameters
        ----------
        ctx : discord.Context

        pref : string
            String with prefered prefix
        """
        with open("./config/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = pref

        with open("./config/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)


def setup(bot):
    bot.add_cog(Prefixes(bot))
