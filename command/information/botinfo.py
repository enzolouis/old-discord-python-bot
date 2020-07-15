import discord

from discord.ext import commands
from datetime import datetime
 
  
  
@commands.command(aliases=["bot-info"])
async def botinfo(ctx):
  embed = discord.Embed(title="Bot informations", color=0x0000bf, timestamp=datetime.utcnow())
  embed.add_field(name="➔ Creators", value="Enzo & ZedRoff")
  embed.add_field(name="➔ Ping", value=round(ctx.bot.latency * 1000))
  embed.add_field(name="➔ Prefix", value="".join(await ctx.bot.command_prefix(ctx.bot, ctx.message)))
  embed.add_field(name="➔ Name", value=ctx.bot.user)
  embed.add_field(name="➔ Mention", value=ctx.bot.user.mention)
  embed.add_field(name="➔ ID", value=ctx.bot.user.id)
  embed.add_field(name="➔ Servers", value=len(ctx.bot.guilds))
  embed.add_field(name="➔ Users", value=len(ctx.bot.users))
  embed.set_thumbnail(url=ctx.bot.user.avatar_url)
  embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
  
  await ctx.send(embed=embed)
  
