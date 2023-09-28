import base64
import discord

from discord.ext import commands

@commands.command(brief="Encode a text to base 64")
async def b64encode(ctx, *, body):
	try:
		await ctx.send(embed=discord.Embed(description=base64.b64encode(body)))
	except Exception as e:
		await ctx.send(f"{e}\n{type(e)}")
		print(e, type(e))

@commands.command(brief="Decode a text from base 64")
async def b64decode(ctx, *, body):
	try:
		await ctx.send(embed=discord.Embed(description=str(base64.b64decode(body), "utf8")))
	except Exception as e:
		await ctx.send(f"{e}\n{type(e)}")