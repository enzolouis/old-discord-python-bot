import typing
import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, members:typing.Union[discord.Member, str], role:discord.Role):
  if members == "all":
    members = [member for member in ctx.guild.members]
    
    for member in members:
      try:
        await member.remove_roles(role)
      except:
        await ctx.send(embed=ERROR(f"Le rôle {role} ne peut pas être enlevé"))
        return
    await ctx.send(embed=GOOD_USE(f"Le rôle {role} a été enlevé à tous les membres avec succès !"))
  
  else:
    if role not in members.roles:
        await ctx.send(embed=ERROR(f"{members} n'a pas le rôle {role}"))
        return
    try:
      await members.remove_roles(role)
    except:
      await ctx.send(embed=ERROR(f"Le rôle {role} ne peut pas être enlevé"))
    else:
      await ctx.send(embed=GOOD_USE(f"Le rôle {role} a été enlevé à {members} avec succès !"))
