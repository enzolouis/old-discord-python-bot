import typing
import asyncio
import io
import traceback
import aiohttp
import os
import sys
import discord
import time

from datetime import timedelta
from textwrap import indent
from contextlib import redirect_stdout
from discord.ext import commands


owner_id = (418154142175854613, 327074335238127616, 684117553974345730, 538056220200796162) # ember, zedroff, doduo


class Eval(commands.Cog):
    """
    Evaluate your code asynchronously with bot action like create channel, ...
    You can return an object, if this object is not None surely, you will have (with your output) 
    the return description with the object, his type, lenght, and dir
    """
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id in owner_id

    @staticmethod
    def py(text):
        """ Format text to a python markdown """
        return f"```py\n{text}\n```"


    async def wait_until_react(self, ctx, msg):
        """ Add reaction :boom: to the return value, if the author click on, the return will be deleted """
        await msg.add_reaction("\N{COLLISION SYMBOL}")

        def check(react, author):
            return author == ctx.author and str(react.emoji) == "\N{COLLISION SYMBOL}" and react.message.id == msg.id
        
        try:
            react = await self.bot.wait_for("reaction_add", check=check, timeout=60)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
        else:
            await msg.delete()


    @commands.command(name="eval", hidden=True)
    async def _eval(self, ctx, *, code): # _eval to don't bloc eval() builtin function
        "Try your python codes directly on discord"
        # :white_check_mark: and :x: in discord
        tick = "\N{WHITE HEAVY CHECK MARK}" # unicode : "\u2049"
        error = "\N{CROSS MARK}" # unicode : "\u2705"

        py = Eval.py # quickly

        env = {
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "bot":self.bot,
        }

        env.update(globals()) # push `env` dictionnary to the globals() builtin dictionnary



        buffer = io.StringIO()

        # create asynchrnous fonction environment to execute await instruction.
        async_code = f"async def func():\n{indent(code, '    ')}"
        # using textwrap :
        # async def func():
        #    code
        #    code
        # not using textwrap :
        # async def fucn():
        # code
        # code
        # INVALID SYNTAX

        try:
            with redirect_stdout(buffer): # SURELY OPTIONNAL BUT SAFE | redirect only stdout and don't send in console, only in discord
                exec(async_code, env) # exec async code with env, in order to have an acces  to variable like ctx, bot, ... (see `env` var)

        except Exception as e: # catch invalid syntax
            msg = await ctx.send(py(f"{e.__class__.__name__}: {e}"))
            await ctx.message.add_reaction(error)
            return await self.wait_until_react(ctx, msg) # even if error happen, :boom: react must be here

        func = env['func'] # get func from env. func is in env at this line : exec(code, env)
        try:
            with redirect_stdout(buffer): # redirect only stdout and don't send in console, only in discord
                return_ = await func()
        except Exception as e:
            value = buffer.getvalue()
            msg = await ctx.send(py(f"{value}{traceback.format_exc()}")) # traceback.format_exc to retrace context exception
            await ctx.message.add_reaction(error)
            return await self.wait_until_react(ctx, msg) # even if error happen, :boom: react must be here
        
        # if 0 error :

        value = buffer.getvalue()

        if return_ is None and not value:
            return await ctx.message.add_reaction(tick)

        to_send = ""

        if value:
            to_send = value
        if return_ is not None:

            to_send = to_send + f"\n\n<Return>\n{return_}\nlenght:{len(return_) if isinstance(return_, typing.Sequence) else len(str(return_))}\n\n<Return type>\n{return_.__class__.__name__}\n\n<Return dir>\n{dir(return_)}"
        

        if len(to_send) < 1980:
            msg = await ctx.send(py(to_send))
            await ctx.message.add_reaction(tick)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://bin.drlazor.be/", data={"val":to_send}) as response:
                    if response.status == 200: # si la requête est réussie
                        # convert = await response.text()
                        msg = await ctx.send(f"<{response.url}>")
                    else:
                        return await ctx.send("Problem with <http://bin.drlazor.be>...")
        
        await self.wait_until_react(ctx, msg)




# rendre hidden chacunes des commandes de ce fichier dans le help (hidden=True)

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.launch = time.monotonic()

    async def cog_check(self, ctx):
        return ctx.author.id in owner_id

    @commands.group()
    async def exa(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Form : `exa` <command>\n__Commands__\n\n`reload`;`shutdown`;`stats`")

    @commands.command()
    async def reload(self, ctx):
        await ctx.send("**Reload...** :warning:")
        os.system("py main.py")
        await self.bot.logout()

    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("**Shutdown...** :x:")
        await self.bot.logout()

    @commands.command()
    async def stats(self, ctx):
        embed = discord.Embed(title=self.bot.user.name)
        embed.add_field(name="Last launch", value=timedelta(seconds=time.monotonic() - self.launch))
        embed.add_field(name="Python version", value=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        embed.add_field(name="discord.py version", value=discord.__version__)
        await ctx.send(embed=embed)


async def setup(bot):
    owner = Owner(bot)
    owner.exa.add_command(owner.reload)
    owner.exa.add_command(owner.shutdown)
    owner.exa.add_command(owner.stats)

    await bot.add_cog(owner)
    await bot.add_cog(Eval(bot))