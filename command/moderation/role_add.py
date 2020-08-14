import typing
import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, members:typing.Union[discord.Member, str], role:discord.Role):
  if members == "all":
    members = [member for member in ctx.guild.members]
    
    for member in members:
      try:
        await member.add_roles(role)
      except:
        await ctx.send(embed=ERROR(f"Le rôle {role} ne peut pas être donné"))
        return
    await ctx.send(embed=GOOD_USE(f"Le rôle {role} a été donné à tous les membres avec succès !"))
  
  else:
    if role in members.roles:
        await ctx.send(embed=ERROR(f"{members} a déja le rôle {role}"))
        return
    try:
      await members.add_roles(role)
    except:
      await ctx.send(embed=ERROR(f"Le rôle {role} ne peut pas être donné"))
    else:
      await ctx.send(embed=GOOD_USE(f"Le rôle {role} a été donné à {members} avec succès !"))
