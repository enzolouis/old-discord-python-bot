import typing
import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed
  
@commands.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, channel: typing.Optional[discord.TextChannel], delay:typing.Union[int, str]):
  channel = channel or ctx.channel
  if delay == 0:
    delay = "off"

  if isinstance(delay, int):
    if 0 < delay <= 21600:
      try:
        await channel.edit(slowmode_delay=delay)
      except: # except because of discord.py bug : __new__() got an unexpected keyword argument 'allow_new' 
        pass

      await ctx.send(f"Slowmode {channel.mention} : :white_check_mark: {delay}")
    else:
      await ctx.send(embed=ERROR("Slowmode have to be from 0 to 21600 seconds maximum"))
      
  
  else:
    if delay == "off":
      await channel.edit(slowmode_delay=0)
      await ctx.send(f"Slowmode {channel.mention} : :x: OFF")
    else:
      await ctx.send(embed=ERROR("Renseignez un nombre de secondes pour activer le slowmode ou \"off\" pour le désactiver !"))
