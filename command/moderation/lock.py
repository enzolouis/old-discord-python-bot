import discord

from discord.ext import commands

from ..error import GOOD_USE

@commands.command()
@commands.has_permissions(manage_messages=True)
async def lock(ctx):
  await ctx.channel.edit(overwrites={ctx.guild.default_role : discord.PermissionOverwrite(send_messages=False, read_messages=ctx.guild.default_role)}) #idée : see_messages=default_role.owerwrite(..) # par défaut en gros
  await ctx.send(embed=GOOD_USE("Le channel est bloqué !"))
  
@commands.command()
@commands.has_permissions(manage_messages=True)
async def unlock(ctx):
  await ctx.channel.edit(overwrites={ctx.guild.default_role : discord.PermissionOverwrite(send_messages=True)})
  await ctx.send(embed=GOOD_USE("Le channel n'est plus bloqué !"))
