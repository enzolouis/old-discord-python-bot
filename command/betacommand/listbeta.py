import discord

from discord.ext import commands

from ..error import *

@commands.command(name="list", brief="Show a list of items in the server : channels, roles, emojis and bots.")
async def list_(ctx):
    channels = []
    for cat in ctx.guild.categories:
        channels.append(str(cat))
        for channel in cat.channels:
            channels.append(f"\t\t{channel}")


    # pas besoin de "Aucun" pour channels et roles
    channels = "\n".join(channels)
    roles = "\n".join([x.name for x in ctx.guild.roles])
    emojis = "".join([str(x) for x in ctx.guild.emojis])
    bots = "\n".join([x.name for x in ctx.guild.members if x.bot])
    members = "\n".join([x.name for x in ctx.guild.members if not x.bot])

    await pag_desc(ctx, 
        f"""**Channels**\n```fix\n{channels or "0 channel in category"}```
**Roles**\n```fix\n{roles}```
**Emojis**\n{emojis or "None"}
**Bots**\n```fix{bots or "None"}```
**Members**\n```fix{members or "None"}```""")