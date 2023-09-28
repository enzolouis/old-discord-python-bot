import discord

from discord.ext import commands

@commands.command(aliases=["size", "lenghten"], brief="Count how many char a paragraph containt")
async def length(ctx, *,  sentence):
	await ctx.send(f"**Sentence char count : {len(sentence)}**")

@commands.command(alias=["sizeword"], brief="Count how many char a paragraph containt")
async def lengthword(ctx, *, sentence):
	await ctx.send(f"**Sentence word count : {len(sentence.split())}**")