import discord

from discord.ext import commands
from random import choice


@commands.command(name="8ball")
async def ball8(ctx, *, message): 
  luck = choice(
                  (
        ("Yes", 0x2eff00), ("Of course !", 0x2eff00), ("Probably", 0x2eff00),
        ("No", 0xDB1702), ("I'm not sure about that...", 0xDB1702), ("Never !", 0xDB1702),
        ("I don't know...", 0xffc900), ("Maybe", 0xffc900), ("What did you say ?", 0xDB1702),
      )
  )
  
  embed = discord.Embed(description=">>> "+message, color=luck[1])
  embed.set_author(name=luck[0])
  await ctx.send(embed=embed)