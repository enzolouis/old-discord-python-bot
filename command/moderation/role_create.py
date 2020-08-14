import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed

  
@commands.command(name="create-role")
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, position:int=1, *, name="New role"): # 0 : textchannel 1 : voicechannel 2 : category
  if position < 1:
    return await ctx.send(embed=ERROR("Merci d'indiquer un nombre supérieur à 0"))

  try:
    role = await ctx.guild.create_role(name=name, reason="Command `create-role`")
    await role.edit(position=position)
  except:
    await ctx.send(embed=ERROR_PERMISSIONS_BOT())
  else:
    await ctx.send(embed=GOOD_USE("Le rôle a bien été créé"))
