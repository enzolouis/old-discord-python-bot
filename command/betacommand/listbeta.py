import discord

from discord.ext import commands

@commands.command()
async def list(ctx):
  channels = []
  for cat in ctx.guild.categories:
    channels.append(str(cat))
    for channel in cat.channels:
      channels.append(f"\t\t{channel}")
  
  
  # pas besoin de "Aucun" pour channels et roles
  channels = "\n".join(channels)
  roles = "\n".join([x.name for x in ctx.guild.roles])
  emojis = "".join([str(x) for x in ctx.guild.emojis])
  bots = "\n".join([x.name for x in ctx.guild.members if x.bot])
  
  await ctx.send(f"> **Channels**\n ```fix\n{channels if channels else '0 channel in category'}```")
  await ctx.send(f"> **Roles**\n ```fix\n{roles[:1990]}```")
  await ctx.send(f"```fix\n{roles[1990:3980]}```")
  await ctx.send(f"> **Emojis**\n {emojis or 'Aucun'}")
  await ctx.send(f"> **Bots**\n ```fix\n{bots or 'Aucun'}```")
  