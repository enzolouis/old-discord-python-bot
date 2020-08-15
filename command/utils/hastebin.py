import discord
import aiohttp

from discord.ext import commands

from ..error import ERROR

@commands.command()
@commands.cooldown(1, 60)
async def hastebin(ctx, *, body):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://hastebin.com/documents", data=body) as response:
            if not response.status == 200: # si la requête est réussie
                return await ctx.send(embed=ERROR("Problem while requesting to hastebin."))
            code = (await response.json())["key"]

            await ctx.send(f":white_check_mark: https://hastebin.com/{code}")