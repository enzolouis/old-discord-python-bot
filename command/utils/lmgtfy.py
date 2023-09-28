import discord

from discord.ext import commands

from ..error import GOOD_USE

@commands.command(brief="The power of lmgtfy...!")
async def lmgtfy(ctx, *, search):
  good_search = "+".join(search.split(" "))
  await ctx.send(embed=GOOD_USE(f"https://www.lmgtfy.com/?q={good_search}"))
