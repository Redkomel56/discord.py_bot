import discord
import time
from discord.ext import commands
import config


class Moder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('moder is ready')

    @commands.command()
    @commands.has_any_role(config.admin_id_role)
    async def mute(self, ctx, user: discord.Member, reason=None):

        channel = self.bot.get_channel(config.log_mes_channel_id)
        guild = self.bot.get_guild(config.recurring_guild_id)
        role = guild.get_role(config.id_mute_role)

        embed = discord.Embed(title=f"Пользователя {user} заглушили", color=0xfac400)
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="Причина:", value=f"{reason}", inline=True)
        embed.set_footer(text=f"BOT • {time.asctime()}")

        await user.add_roles(role)

        await channel.send(embed=embed)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed, delete_after=30)


    @commands.command()
    @commands.has_any_role(config.admin_id_role)
    async def unmute(self, ctx, user: discord.Member):

        channel = self.bot.get_channel(config.log_mes_channel_id)
        guild = self.bot.get_guild(config.recurring_guild_id)
        role = guild.get_role(config.id_mute_role)

        embed = discord.Embed(title=f"Пользователя {user} разглушили", color=0xfac400)
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"BOT • {time.asctime()}")

        await user.remove_roles(role)

        await channel.send(embed=embed)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed, delete_after=30)


    @commands.command()
    @commands.has_any_role(config.admin_id_role)
    async def ban(self, ctx, user: discord.Member, *, reason=None):

        channel = self.bot.get_channel(config.log_mes_channel_id)

        embed = discord.Embed(title=f"Пользователя {user} забанили", color=0xfac400)
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="Причина:", value=f"{reason}", inline=True)
        embed.set_footer(text=f"BOT • {time.asctime()}")

        await channel.send(embed=embed)
        await user.ban(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed, delete_after=30)


    @commands.command()
    @commands.has_any_role(config.admin_id_role)
    async def unban(self, ctx, *, member):

        banned_users = await ctx.guild.bans()
        channel = self.bot.get_channel(config.log_mes_channel_id)

        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title=f"Пользователя {user} разбанили", color=0xfac400)
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=f"Silence. • {time.asctime()}")
                await channel.send(embed=embed)
                await ctx.channel.purge(limit=1)
                await ctx.send(embed=embed, delete_after=30)
                return


    @commands.command()
    @commands.has_any_role(config.admin_id_role)
    async def kick(self, ctx, user: discord.Member, *, reason=""):

        channel = self.bot.get_channel(config.log_mes_channel_id)

        embed = discord.Embed(title=f"Пользователя {user} выгнали из сервера", color=0xfac400)
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="Причина:", value=f"{reason}", inline=True)
        embed.set_footer(text=f"BOT • {time.asctime()}")

        await channel.send(embed=embed)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed, delete_after=30)
        await user.kick()



    @commands.command()
    @commands.has_any_role(config.admin_id_role)
    async def clear(self, ctx, amount=20):

        channel = self.bot.get_channel(config.log_mes_channel_id)
        if amount < 200:

            embed = discord.Embed(title=f"Очистил чат \"{ctx.channel}\" на {amount} сообщений(ия)", color=0xfac400)
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"BOT • {time.asctime()}")

            await ctx.channel.purge(limit=int(amount))
            await channel.send(embed=embed)
            await ctx.send(embed=discord.Embed(description=f":wheelchair: удалено {amount} сообщений(я)"), delete_after=30)
        else:
            await ctx.send(embed=discord.Embed(description=f":Вы не можете удалить больше 200 сообщений"), delete_after=30)


async def setup(bot):
    await bot.add_cog(Moder(bot))
