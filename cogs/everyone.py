import discord
import time
import config
from discord.ext import commands


class Everyone(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('everyone is ready')

	@commands.command()
	async def info(self, ctx):
		embed = discord.Embed(title=f">>     Команды     <<",  color=0x9370DB)
		embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")

		embed.add_field(name=f"***{config.prefix}mute*** --- отключить возможность говорить и писать человеку", value=f"Пример: {config.prefix}mute @1234", inline=False)
		embed.add_field(name=f"***{config.prefix}unmute*** --- вернуть все возможности человку", value=f"Пример: {config.prefix}unmute @1234", inline=False)
		embed.add_field(name=f"***{config.prefix}ban*** --- добавить человека в черный список и выгнать", value=f"Пример: {config.prefix}ban @1234", inline=False)
		embed.add_field(name=f"***{config.prefix}unban*** --- убрать человека из чероного списка", value=f"Пример: {config.prefix}unban @1234", inline=False)
		embed.add_field(name=f"***{config.prefix}kick*** --- выгрнать человека", value=f"Пример: {config.prefix}kick @1234", inline=False)
		embed.add_field(name=f"***{config.prefix}clear*** --- удалить последние сообщения", value=f"Пример: {config.prefix}clear 40", inline=False)

		embed.set_footer(text=f"BOT • {time.asctime()}")
		await ctx.channel.purge(limit=1)
		await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Everyone(bot))
