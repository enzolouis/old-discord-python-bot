import typing
import discord

from discord.ext import commands
from random import randint

@commands.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, channel: typing.Optional[discord.TextChannel], *, message):
  await ctx.message.delete()
  channel = channel or ctx.channel
  embed = discord.Embed(description=message, color=randint(0, 0xffffff)) # random
  await channel.send(embed=embed)