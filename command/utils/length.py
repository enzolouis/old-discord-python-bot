import discord

from discord.ext import commands

@commands.command(aliases=["size", "lenghten"])
async def length(ctx, *,  sentence):
	await ctx.send(f"**Sentence char count : {len(sentence)}**")

@commands.command()
async def lengthword(ctx, *, sentence):
	await ctx.send(f"**Sentence word count : {len(sentence.split())}**")