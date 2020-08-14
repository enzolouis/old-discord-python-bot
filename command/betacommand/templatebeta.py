import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed

""" Admin """
@commands.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def template(ctx, the_template):
  templates = ("rp", "informatique", "gaming")
  temp = the_template.lower()
  
  if not temp in templates:
    await ctx.send("**Vous avez indiqué une mauvaise template**")
    await ctx.send(embed=GOOD_USE("```diff\nListe des templates :\n- rp\n- informatique\n- gaming```"))
    return

  # si la template existe
  
  def check(message):
    return message.content == "oui" and message.author == ctx.author
    
  try:
    await ctx.send("Si vous générez une template, tous le serveur va être remis à 0 (salons, rôles, ...) et la template va se générer. \
    \n**Envoyez \"oui\" si vous le voulez.**")
    await bot.wait_for("message", check=check, timeout=15)
  except asyncio.TimeoutError:
    await ctx.send("**Vous n'avez pas choisi à temps !**")
    return
  else:
    await ctx.send(f"**La template sur le thème \"{temp}\" se génère...")
  
  for x in ctx.guild.channels:
    await x.delete()
  for x in ctx.guild.roles:
    try:
      await x.delete()
    except:
      pass
  
  if temp == "rp":
    pass
    


@template.error
async def template_error(ctx, error):
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send(embed=BLUE_EMBED("```diff\nListe des templates :\n- rp\n- informatique\n- gaming```"))