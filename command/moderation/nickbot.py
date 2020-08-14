import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command()
@commands.has_permissions(manage_nicknames=True)
async def nickbot(ctx, *, new_nick):
  try:                           
    await ctx.guild.get_member(ctx.bot.user.id).edit(nick=new_nick)
  except discord.errors.HTTPException:
    await ctx.send(embed=ERROR("Le nom est trop long !"))