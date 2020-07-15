import aiohttp
import discord

from discord.ext import commands

from ..error import CtxEmbed


@commands.command()
async def cat(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get("http://aws.random.cat/meow") as response:
        if response.status == 200: # si la requête est réussie
            convert = await response.json()
            embed = CtxEmbed(ctx, title="Cat random picture")
            embed.set_image(url=convert["file"])
            await ctx.send(embed=embed)