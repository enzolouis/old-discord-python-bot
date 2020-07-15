import discord

from discord.ext import commands


@commands.command(enabled=False)
async def ping(ctx):
  await ctx.send(embed=GOOD_USE(f"Ping: {round(ctx.bot.latencies[ctx.guild.shard_id][1] * 1000, 3)}ms"))