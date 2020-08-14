import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command(name="create-channel")
@commands.has_permissions(manage_channels=True)
async def create_channel(ctx, type:int, *, name="New channel"): # 0 : textchannel 1 : voicechannel 2 : category
  if type==1:
    await ctx.guild.create_text_channel(name, reason="Command `create-channel`")
  elif type==2:
    await ctx.guild.create_voice_channel(name, reason="Command `create-channel`")
  elif type==3:
    await ctx.guild.create_category(name, reason="Command `create-channel`")
  else:
    return await ctx.send("Merci d'indiquer le type **1(text channel), 2(voice channel) ou 3(category)**")
  
  
  await ctx.send(embed=GOOD_USE("Le salon a bien été créé"))