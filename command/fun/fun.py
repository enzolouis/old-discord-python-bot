import asyncio
import discord
import aiohttp

from discord.ext import commands
from random import randint, choice

from ..error import *

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="Generate a random number between 1 to infinity !")
    async def roll(self, ctx, nbr:int):
        if nbr < 1:
            return await ctx.send("**Please type a `number` < 0**")

        embed = discord.Embed(description=randint(1, nbr))
        await ctx.send(embed=embed)

    @commands.command(name="8ball", brief="Say something, bot answer what he think !")
    async def ball8(self, ctx, *, message): 
        luck = choice(
                (
            ("Yes", 0x2eff00), ("Of course !", 0x2eff00), ("Probably", 0x2eff00),
            ("No", 0xDB1702), ("I'm not sure about that...", 0xDB1702), ("Never !", 0xDB1702),
            ("I don't know...", 0xffc900), ("Maybe", 0xffc900), ("What did you say ?", 0xDB1702),
          )
        )

        embed = discord.Embed(description=">>> "+message, color=luck[1])
        embed.set_author(name=luck[0])
        await ctx.send(embed=embed)


    @commands.command(brief="Look at this dogs !")
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://random.dog/woof.json") as response:
                if response.status == 200: # si la requête est réussie
                    convert = await response.json()
                    embed = CtxEmbed(ctx, title="Dog random picture")
                    embed.set_image(url=convert["url"])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(embed=ERROR("There was an error while requesting the picture."))

    @commands.command(brief="Look at this cats !")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as response:
                if response.status == 200: # si la requête est réussie
                    convert = await response.json()
                    embed = CtxEmbed(ctx, title="Cat random picture")
                    embed.set_image(url=convert["file"])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(embed=ERROR("There was an error while requesting the picture."))


    @commands.command(brief="Generate a random number between 1 to infinity, and all users must find it to win ! You can specify a time in seconds after the number. By default, this time is 300, 300 seconds to find the number")
    async def bingo(self, ctx, number:int, time_seconds:int=300):
        if number < 1:
            return await ctx.send("**Please type a `number` < 0**")
        if time_seconds > 10000:
            return await ctx.send(f"**Please don't enter a too big time ({time_seconds}), the maximum is 10000...**")

        random_nbr = randint(1, number)
        await ctx.send(embed=GOOD_USE(f"Bingo from 1 to {number} ! You have {time_seconds} seconds to find it."))

        def check(message):
            if is_positive_integer(message.content):
                return int(message.content) == random_nbr and message.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=time_seconds)
        except asyncio.TimeoutError:
            return await ctx.send(embed=ERROR(f"You lost ! The right number was **{random_nbr}**"))
        await ctx.send(embed=GOOD_USE(f"{msg.author.mention} won ! The right number was **{random_nbr}**"))



    @commands.command(brief="Generate a random number between 1 to infinity, and all users must find it to win ! It's a an advanced bingo \
        command. The user receive by the bot if his number was superior or inferior to the number")
    async def breakbingo(self, ctx, number:int):
        if number < 1:
            return await ctx.send("**Please type a `number` < 0**")
      
        random_nbr = randint(1, number)
        await ctx.send(embed=GOOD_USE(f"Advanced bingo between 1 to {number} ! (:warning: THSI BINGO IS NEVER STOP WHILE MEMBERS SEND MESSAGE IN THE CHANNEL, YOU CAN BREAK IT BY TYPING \"stop\" in the chat)"))
      
      
        def check(message):
            return message.channel == ctx.channel and (is_positive_integer(message.content) or message.content in ["stop", "break", "cancel"])
      
        while True:
            try:
                bingo = await self.bot.wait_for("message", check=check, timeout=50)

                if bingo.content in ["stop", "break", "cancel"]:
                    if bingo.author == ctx.author or bingo.author.guild_permissions.administrator:
                        return await ctx.send(embed=WARNING(f"This bingo was ended. The right number was **{random_nbr}**"))
                    else:
                        await ctx.send(embed=ERROR(f"{bingo.author.mention}, you can't stop this game. Only {ctx.author.mention} and administrator can."))
                        continue
              
                bingo_content = int(bingo.content)
                if random_nbr == bingo_content:
                    return await ctx.send(embed=GOOD_USE(f"{bingo.author.mention} won ! The right number was **{random_nbr}**"))
                await ctx.send(f"{bingo.author.name} ({bingo_content}) : " + (":arrow_up:" if random_nbr > int(bingo.content) else ":arrow_down:"))
          
            except asyncio.TimeoutError:
                return await ctx.send(embed=ERROR(f"You lost ! The right number was **{random_nbr}**"))



async def setup(bot):
    await bot.add_cog(Fun(bot))