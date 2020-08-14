import asyncio
import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command(name="rename-prefix")
@commands.has_permissions(manage_nicknames=True)
async def rename_prefix(ctx, new_prefix):
  
  await ctx.send(embed=WARNING("""**Entrez 1 si :** vous voulez réinitialiser le surnom de TOUS les utilisateurs et leurs ajouter un prefix.\n
  **Entrez 2 si :** vous voulez seulement leur ajouter un prefix (Attention, si vous faîtes la commande plusieurs fois, les préfix vont s'accumuler, mais les surnoms vont restés) ?"""))
  
  def check(message):
    return message.author == ctx.author and (message.content == "1" or message.content == "2")
  try:
    choice = await ctx.bot.wait_for("message", check=check, timeout=60)
  except asyncio.TimeoutError:
    return await ctx.send("Temps écoulé.")
  
  for member in ctx.guild.members:
    try:
      if choice.content == "1":
        await member.edit(nick=new_prefix + " " + member.name)
      elif choice.content == "2":
        await member.edit(nick=new_prefix + " " + (member.nick or member.name))
    except:
      pass
  await ctx.send(embed=GOOD_USE(f"J'ai ajouté le préfix {new_prefix} au pseudo de tous les membres (sauf ceux situés au-dessus de mon rôle)"))
