import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command()
@commands.has_permissions(manage_nicknames=True)
async def rename(ctx, members:commands.Greedy[discord.Member], *, new_nick):
  try:
    for member in members:
      try:
        await member.edit(nick=new_nick)
      except discord.errors.Forbidden:
        await ctx.send(f":x: {member} (Je n'ai pas la permission)", delete_after=5)
      else:
        await ctx.send(f":white_check_mark: {member}", delete_after=5)
    
  except discord.errors.HTTPException:
    await ctx.send(embed=ERROR(":x: Le nom est trop long !"))
   