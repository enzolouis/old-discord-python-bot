import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, reason="None"):
  try:
    await member.kick(reason=reason)
  except discord.errors.Forbidden:
    await ctx.send(embed=ERROR_PERMISSIONS_BOT())
  else:
    await ctx.send(embed=GOOD_USE(f"{member.name} ({member.id}) a été expulsé du serveur.\n Raison : *{reason}*"))
    