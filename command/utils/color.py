import discord

from discord.ext import commands
from PIL import Image

@commands.command()
async def color(ctx, hexa):
  hexa = hexa.lstrip("#")
  try:
    rgb = tuple([int(hexa[i:i+2], 16) for i in (0, 2, 4)])
  except:
    await ctx.send(embed=ERROR("Le format ne convient pas !\nMerci d'indiquer un nombre en base 16 (héxadécimal)"))
  else:
    img = Image.new("RGB",(150, 150), rgb) # pas obligé de renseigner du RGB en paramètre
    img.save("command/utils/color.png")
    file = discord.File("command/utils/color.png", filename="color.png")
    embed = discord.Embed(description=f"#{hexa[:6]} | RGB : {rgb}", color=int(hexa, 16)) # convert hexadecimal to int (without "0x"), to get the 0x... after, hex() all
    embed.set_image(url="attachment://color.png")
    await ctx.send(file=file, embed=embed)

