import discord

from discord.ext import commands
from datetime import datetime

@commands.command(aliases=["user-info"])
async def userinfo(ctx, member:discord.Member=None):
  if member is None:
    member = ctx.guild.get_member(ctx.author.id) # what ?
    
  roles = [x.name for x in member.roles]

  embed = discord.Embed(title=f"{member}'s informations", color=0x0000bf, timestamp=datetime.utcnow())
  embed.add_field(name="➔ Name", value=member)
  embed.add_field(name="➔ Mention", value=member.mention)
  embed.add_field(name="➔ ID", value=member.id)
  create = member.created_at
  create = "/".join((str(create.day), str(create.month), str(create.year)))
  embed.add_field(name="➔ Account creation", value=create)
  embed.add_field(name="➔ Activity", value=member.activity)
  embed.add_field(name="➔ Status", value=member.status)
  join = member.joined_at
  join = "/".join((str(join.day), str(join.month), str(join.year)))
  embed.add_field(name="➔ Server join", value=join)
  embed.add_field(name="➔ Higher role", value=member.top_role.name)
  embed.add_field(name="➔ Roles", value=" - ".join(roles))
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)