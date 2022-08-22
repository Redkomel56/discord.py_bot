import asyncio
import os
import discord
from discord.ext import commands
import config


discord_intents = discord.Intents.all()
discord_intents.members = True

bot = commands.Bot(command_prefix=config.prefix, intents=discord_intents)
bot.remove_command("help")


@bot.event
@commands.has_any_role(*config.admin_id_role)
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(config.prefix+"info"))
    await bot.wait_until_ready()



@bot.command()
@commands.has_any_role(*config.admin_id_role)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    print(f"load module: cogs.{extension}")


@bot.command()
@commands.has_any_role(*config.admin_id_role)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"unload module: cogs.{extension}")


@bot.command()
@commands.has_any_role(*config.admin_id_role)
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print(f"reload module: cogs.{extension}")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    print('zit goot')
    await load_extensions()
    await bot.start(config.token)



if __name__ == "__main__":
    # bot.run(config.token)
    asyncio.run(main())
