import discord
from discord.ext import commands
import asyncio
import typing

from random import randint

from ..error import *
from ..emojis import *

class Sanctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        await ctx.message.delete()
        bans = await ctx.guild.bans()
        embed = CtxEmbed(ctx)
        if not bans:
            embed.description = "No ban"
            await ctx.send(embed=embed)
        else:
            # embed.description = 
            await pag_desc(ctx, "\n".join([f"{ban.user.name} ({ban.user.id})" for ban in bans]))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason="None"):
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.send(embed=ERROR_PUNISHMENTS("ban"))

        await member.ban(reason=reason)
        await ctx.send(embed=GOOD_USE(f"{member.name} ({member.id}) has been banned from the server.\n Reason : *{reason}*"))


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id:int, *, reason="None"):
        bans = await ctx.guild.bans()

        for x in range(len(bans)):
            ban = bans[x].user
            if ban.id == user_id:
                await ctx.guild.unban(ban, reason=reason)
                return await ctx.send(embed=GOOD_USE(f"{ban} ({ban.id}) has been unbanned for the reason {reason}."))
                

        await ctx.send(embed=ERROR(f"ID {user_id} not found in users banned"))


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *, reason="None"):
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.send(embed=ERROR_PUNISHMENTS("kick"))

        await member.kick(reason=reason)
        await ctx.send(embed=GOOD_USE(f"{member.name} ({member.id}) has been kicked from the server.\n Reason : *{reason}*"))
    

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member:discord.Member):
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.send(embed=ERROR_PUNISHMENTS("mute"))

        for x in ctx.guild.text_channels:
            if x.permissions_for(member).send_messages:
                await x.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages=False, read_messages=x.permissions_for(member).read_messages))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member:discord.Member):
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.send(embed=ERROR_PUNISHMENTS("unmute"))

        for x in ctx.guild.text_channels:
            if not x.permissions_for(member).send_messages:
                await x.set_permissions(member, overwrite=None) # delete member's overwrite in channel

    async def get_lock_info(self, ctx, channel, reason):
        channel = channel or ctx.channel
        reason = f"for the reason : *{reason[:2000]}*" if reason is not None else "" # 2000 to not exceeded description max size

        return channel, reason


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, channel:discord.TextChannel=None, reason=None): # ajouter l'option de lock un autre channel typing.Optional[discord.Channel]=None
        channel, reason = self.get_lock_info(ctx, channel, reason)

        await channel.edit(overwrites={ctx.guild.default_role : discord.PermissionOverwrite(send_messages=False, read_messages=channel.overwrites_for(ctx.guild.default_role).read_messages)}) #idée : see_messages=default_role.owerwrite(..) # par défaut en gros
        await channel.send(embed=GOOD_USE(f"Channel locked by {ctx.author} {reason}"))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel:discord.TextChannel=None, reason=None):
        channel, reason = self.get_lock_info(ctx, channel, reason)

        await channel.edit(overwrites={ctx.guild.default_role : discord.PermissionOverwrite(send_messages=True, read_messages=channel.overwrites_for(ctx.guild.default_role).read_messages)})
        await channel.send(embed=GOOD_USE(f"Channel unlocked by {ctx.author} {reason}"))
        

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def templock(self, ctx, channel:typing.Optional[discord.TextChannel], time, reason=None):
        channel, reason = self.get_lock_info(ctx, channel, reason)

        time = format_hours(time)
        if time is None:
            return await ctx.send("Bad time format. Example : `1h`, `10m`, `30s`")
        
        durat, raw_durat = time

        if durat > 720:
            return await ctx.send(f"The lock time limit is 12 hours. {raw_durat} is too long")

        await channel.edit(overwrites={ctx.guild.default_role : discord.PermissionOverwrite(send_messages=False, read_messages=channel.overwrites_for(ctx.guild.default_role).read_messages)}) #idée : see_messages=default_role.owerwrite(..) # par défaut en gros
        await channel.send(embed=GOOD_USE(f"Channel locked by {ctx.author} : `{raw_durat}` {reason}"))

        await asyncio.sleep(durat)

        await channel.edit(overwrites={ctx.guild.default_role : discord.PermissionOverwrite(send_messages=True, read_messages=channel.overwrites_for(ctx.guild.default_role).read_messages)})
        await channel.send(embed=GOOD_USE(f"Channel now unlocked after {raw_durat}"))
        

    @commands.command() 
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, nbr:int):
        await ctx.message.delete()
        if not 2 <= nbr <= 100:
            return await ctx.send(embed=ERROR("Please type a number between 2 to 100"), delete_after=3)
      
        await ctx.channel.purge(limit=nbr)
        await ctx.send(embed=GOOD_USE(f"{nbr} messages deleted !"), delete_after=3)
    

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: typing.Optional[discord.TextChannel], *, message):
        channel = channel or ctx.channel
        embed = discord.Embed(description=message, color=randint(0, 0xffffff)) # random
        await channel.send(embed=embed)
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Sanctions(bot))