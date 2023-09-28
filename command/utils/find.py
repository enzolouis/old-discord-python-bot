import discord

from discord.ext import commands


@commands.command(brief="Find some users with their name and discriminator")
async def find(ctx, user):
  embed = discord.Embed()
  user_find_with_name = []
  for user_ in ctx.bot.users:
    if user.lower() in str(user_).lower():
      user_find_with_name.append(str(user_) + (str("\t(BOT)") if user_.bot else ""))
  embed.title="Utilisateur trouvé avec un nom"
  embed.description="```fix\n"+"\n".join(user_find_with_name)+"```" if user_find_with_name else "None"
  
  try:
    await ctx.send(embed=embed)
  except:
    await ctx.send(embed=ERROR("Trop d'utilisateur trouvé d'un coup !"))
  



