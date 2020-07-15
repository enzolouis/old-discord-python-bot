import pyqrcode
import png
import discord

from discord.ext import commands

from ..error import ERROR

@commands.command()
async def qrcode(ctx, *, message):
  try:
    url = pyqrcode.create(message)
  except:
    return await ctx.send(embed=ERROR("Vous avez renseignés trop de données"))
  url.png("command/utils/qrcode.png", scale=5) # scale : taille de l'image

  file = discord.File("command/utils/qrcode.png")
  await ctx.send(file=file)