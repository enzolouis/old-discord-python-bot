import discord

from discord.ext import commands
from random import randint


@commands.command()
async def roll(ctx, nbr:int):
  if nbr < 1:
    await ctx.send("**Please type a `number` < 0**")
    return
  
  embed = discord.Embed(description=randint(1, nbr))
  await ctx.send(embed=embed)




