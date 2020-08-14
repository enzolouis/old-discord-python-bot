import discord
from discord.ext import commands
import os
import asyncio
from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command()
async def ban(ctx, member:discord.Member, *, reason="None"):
  try:
    await member.ban(reason=reason)
  except discord.errors.Forbidden:
    await ctx.send(embed=ERROR_PERMISSIONS_BOT())
  else:
    await ctx.send(embed=GOOD_USE(f"{member.name} ({member.id}) a été banni du serveur.\n Raison : *{reason}*"))


@commands.command()
async def unban(ctx, member:discord.Member, *, reason="None"):
  try:
    await member.unban(reason=reason)
  except discord.errors.Forbidden:
    await ctx.send(embed=ERROR_PERMISSIONS_BOT())
  else:
    await ctx.send(embed=GOOD_USE(f"{member.name} ({member.id}) a été débanni du serveur.\n Raison : *{reason}*"))
