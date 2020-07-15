import aiohttp
import discord

from discord.ext import commands

from ..error import CtxEmbed


@commands.command()
async def dog(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://random.dog/woof.json") as response:
        if response.status == 200: # si la requête est réussie
            convert = await response.json()
            embed = CtxEmbed(ctx, title="Dog random picture")
            embed.set_image(url=convert["url"])
            await ctx.send(embed=embed)


"""# ou alors mais mauvais pour la gestion asynchrone :
request = requests.get("https://dog.ceo/api/breeds/image/random")
js = request.json()
embed = CtxEmbed(ctx, title="Random dog images")
embed.set_image(url=js["message"])
await ctx.send(embed=embed)"""