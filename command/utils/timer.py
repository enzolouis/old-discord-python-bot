import asyncio
import discord

from discord.ext import commands


@commands.command(brief="Summon a timer between infinity to 0")
async def timer(ctx, *, start:int):
  if start < 1:
    await ctx.send("**Please type a `number` < 0**")
    return
  
  embed = discord.Embed(description=f"```bat\n{start}```")
  timer_ = await ctx.send(embed=embed)
  for x in range(start-1, -1, -1):
    await asyncio.sleep(1)
    embed = discord.Embed(description=f"```bat\n{x}```")
    await timer_.edit(embed=embed)