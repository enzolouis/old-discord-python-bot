import typing
import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command(name="delete-channel")
@commands.has_permissions(manage_channels=True)
async def delete_channel(ctx, channel:typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel]):
  await channel.delete(reason="Command `delete-channel`")
  await ctx.send(embed=GOOD_USE("Le salon a bien été supprimé"))