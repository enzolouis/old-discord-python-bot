import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command(name="delete-role")
@commands.has_permissions(manage_roles=True)
async def delete_role(ctx, role:discord.Role):
  try:
    await role.delete(reason="Command `delete-role`")
  except:
    await ctx.send(f"Je n'ai pas les permissions de supprimer le rôle {role}")
  else:
    await ctx.send(embed=GOOD_USE("Le rôle a bien été supprimé"))
