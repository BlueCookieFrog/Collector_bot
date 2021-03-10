import discord
from discord.ext import commands
import json
import os
import sys


def get_prefix(ctx, message: discord.Message):
    """ Gets prefix for each defined server """

    try:
        with open("./config/prefixes.json", "r") as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except (KeyError, FileNotFoundError):
        fix_missing_key(message.guild)
        return "."

# Defining bot object

bot = commands.Bot(command_prefix=get_prefix)


def fix_missing_key(guild):
    """fixes missing key if prefix wasn't assigned for server"""

    try:
        with open("./config/prefixes.json", "r") as f:
            prefixes = json.load(f)
    except FileNotFoundError:
        prefixes = {}

    prefixes[str(guild.id)] = "."

    with open("./config/prefixes.json", "w+") as f:
        json.dump(prefixes, f, indent=4)


def read_token():
    """ Reads bot token from token.txt file """
    try:
        with open(f"./token.txt", "r") as f:
            lines = f.readlines()
            return lines[0].strip()
    except FileNotFoundError:
        print("No token file was found")
        sys.exit()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Reloads cogs. Allows to reload specific cog or reload/load all cogs avaliable in cog directory.

    Parameters
    ----------
    ctx :
        Discord.py Context class.

    extension : String
        Name of script to reload. Use "all" to reload all cogs existing in ./cogs;
    """
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    bot.unload_extension(f"cogs.{filename[:-3]}")
                except commands.ExtensionNotLoaded:
                    pass
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Reloaded {filename}")
        print(f"Reloaded all")

    else:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        print(f"Reloaded {extension}")


# execution part

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename}")

token = read_token()

bot.run(token)
