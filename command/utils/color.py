import discord

from discord.ext import commands
from PIL import Image

from ..error import ERROR

@commands.command(brief="Find a color with hexadecimal code")
async def color(ctx, hexa):
    hexa = hexa.strip("#")
    try:
        rgb = tuple([int(hexa[i:i+2], 16) for i in (0, 2, 4)])
    except:
        await ctx.send(embed=ERROR("Bad format"))
    else:
        img = Image.new("RGB",(150, 150), rgb) # pas obligé de renseigner du RGB en paramètre
        img.save("command/utils/color.png")
        file = discord.File("command/utils/color.png", filename="color.png")
        embed = discord.Embed(description=f"#{hexa[:6]} | RGB : {rgb}", color=int(hexa, 16)) # convert hexadecimal to int (without "0x"), to get the 0x... after, hex() all
        embed.set_image(url="attachment://color.png")
        await ctx.send(file=file, embed=embed)


@commands.command(brief="Find a rgb code with an hexadecimal code")
async def rgb(ctx, hexa):
    hexa = hexa.strip("#")
    try:
        rgb = tuple([int(hexa[i:i+2], 16) for i in (0, 2, 4)])
    except:
        return await ctx.send(embed=ERROR("Bad hexadecimal format"))
    await ctx.send(f"__Hexadecimal__ : {hexa}\n__RGB__ : {rgb}")

@commands.command(brief="Find an hexadecimal code with a rgb code")
async def hexa(ctx, r:int, g:int, b:int):

    for elt in (r, g, b):
        if elt < 0 or elt > 255:
            return await ctx.send(embed=ERROR(f"{elt} is a bad value. Please enter good RGB values, the three number must be between 0 to 255 !\nExample :\n(123, 34, 122)\n(10, 9, 0)\n(255, 21, 245)"))

    hexa = hex(r << 16 | g << 8 | b)[2:]

    if len(hexa) < 6:
        hexa = "0"*(6-len(hexa)) + hexa # complete 0 to the hexadecimal beginning. whitout this, (0, 0, 0) : #0, with : #000000


    # hexa = f"#{r:02x}{g:02x}{b:02x}" # other way discover
    await ctx.send(f"__RGB__ : {rgb}\n__Hexadecimal__ : #{hexa}")