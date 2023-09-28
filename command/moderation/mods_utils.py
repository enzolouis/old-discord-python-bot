import discord
import asyncio
import typing

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed, is_positive_integer, format_hours


class UtilsMods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-channel")
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, type:int, *, name="New channel"): # 0 : textchannel 1 : voicechannel 2 : category
        if len(name) > 100:
            return await ctx.send(embed=ERROR("The name size must be between 1 to 100"))
        if type==1:
            await ctx.guild.create_text_channel(name, reason="Command `create-channel`")
        elif type==2:
            await ctx.guild.create_voice_channel(name, reason="Command `create-channel`")
        elif type==3:
            await ctx.guild.create_category(name, reason="Command `create-channel`")
        else:
            return await ctx.send("Type must be **1(text channel), 2(voice channel) or 3(category)**")


        await ctx.send(embed=GOOD_USE("Channel created"))

    @commands.command(name="delete-channel")
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, channel:typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel]):
        await channel.delete(reason="Command `delete-channel`")
        await ctx.send(embed=GOOD_USE("Channel deleted"))






async def setup(bot):
    await bot.add_cog(UtilsMods)