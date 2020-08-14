import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR

@commands.command() 
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nbr:int):
  await ctx.message.delete()
  if not 0 < nbr <= 100:
    return await ctx.send(embed=ERROR("Please type a number between 1 and 100"), delete_after=3)
  
  await ctx.channel.purge(limit=nbr)
  await ctx.send(embed=GOOD_USE(f"{nbr} messages effacés !"), delete_after=5)
  