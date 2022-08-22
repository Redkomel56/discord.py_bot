import time
import discord
import config
from discord.ext import commands


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('logs is ready')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.mention != self.bot.user.mention:
            embed = discord.Embed(title=f">>   💔  Удалил сообщение  💔   <<",  color=0xfd4e4e)
            embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
            embed.add_field(name=f"🔰  ***Сообщение:***", value=f"{message.content}", inline=False)
            embed.set_footer(text=f"Silence. • {time.asctime()}")
            
            channel = self.bot.get_channel(config.log_mes_channel_id)
            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        try:
            embed = discord.Embed(title=f">>   🧡  Отредактировал сообщение  🧡   <<",  color=0xFF8C00)
            embed.set_author(name=f"{message_before.author}", icon_url=f"{message_before.author.avatar_url}")
            embed.add_field(name=f"🔰  ***Сообщение до:***", value=f"- {message_before.content}", inline=False)
            embed.add_field(name=f"🔰  ***Сообщение после:***", value=f"- {message_after.content}", inline=False)
            embed.set_footer(text=f"Silence. • {time.asctime()}")

            channel = self.bot.get_channel(config.log_mes_channel_id)
            await channel.send(embed=embed)
        except Exception as ex:
            print("LogError")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title=f">>   💚  Пользователь зашел на сервер  💚   <<",  color=0x7bff51)
        embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"Silence. • {time.asctime()}")

        channel = self.bot.get_channel(config.log_mes_channel_id)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="**>>   💔  Пользователь покинул сервер  💔   <<**", color=0xfd4e4e)
        embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"Silence. • {time.asctime()}")

        channel = self.bot.get_channel(config.log_mes_channel_id)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = self.bot.get_channel(config.log_mes_channel_id)
        guild = self.bot.get_guild(config.recurring_guild_id)
        if before.channel != after.channel:
            if before.channel is None:
                user_channel = guild.get_channel(after.channel.id)
                user_limit = user_channel.user_limit
                members = len(user_channel.members)

                title = f"**>>   💚  Присоединился к голосовому каналу  💚   <<**`{after.channel}`"
                description = f"кол-во человек на канале {members}/{'∞' if user_limit == 0 else user_limit}"
                color = 0x7bff51
            elif after.channel is None:
                title = f"**>>   💔  Вышел из голосового канала  💔   <<**`{before.channel}`"
                description = f"Пользователь вышел"
                color = 0xfd4e4e
            else:
                user_channel = guild.get_channel(after.channel.id)
                user_limit = user_channel.user_limit
                members = len(user_channel.members)

                title = f"**>>   🧡  Сменил голосовой канал с `{before.channel}` на `{after.channel}`  🧡   <<**"
                description = f"кол-во человек на канале {members}/{'∞' if user_limit == 0 else user_limit}"
                color = 0xFF8C00

            embed = discord.Embed(title=title, description=description, color=color)
            embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"Silence. • {time.asctime()}")
            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
