import discord

from discord.ext import commands

from ..error import CtxEmbed


@commands.command(aliases=["server-info"])
@commands.guild_only()
async def serverinfo(ctx):  
  embed = CtxEmbed(ctx, title="Server informations", color=0x0000bf)  
  embed.add_field(name="➔ Name", value=ctx.guild.name)
  embed.add_field(name="➔ ID", value=ctx.guild.id)
  create = ctx.guild.created_at
  create = "/".join((str(create.day), str(create.month), str(create.year)))
  embed.add_field(name="➔ Creation", value=create)
  embed.add_field(name="➔ Member count", value=ctx.guild.member_count) # len(ctx.guild.members)
  embed.add_field(name="➔ Owner", value=ctx.guild.owner)
  embed.add_field(name="➔ Channels", value=len(ctx.guild.channels))
  embed.add_field(name="➔ Roles", value=len(ctx.guild.roles))
  embed.add_field(name="➔ Emojis", value=len(ctx.guild.emojis))
  embed.add_field(name="➔ Region", value=ctx.guild.region)
  embed.add_field(name="➔ AFK channel", value=ctx.guild.afk_channel if ctx.guild.afk_channel else "Aucun")
  nsfw = [x.name for x in ctx.guild.text_channels if x.is_nsfw()]
  embed.add_field(name="➔ NSFW channels", value=len(nsfw) if nsfw else "Aucun")
  
  embed.set_thumbnail(url=ctx.guild.icon_url)
  await ctx.send(embed=embed)
  