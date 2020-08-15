import discord
from discord.ext import commands
import inspect
import io
import textwrap
import traceback
import os
import sys

from contextlib import redirect_stdout

def check(ctx):
    return ctx.author.id == 418154142175854613

import time
from datetime import timedelta
launch = time.monotonic()


# rendre hidden chacunes des commandes de ce fichier dans le help (hidden=True)

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(check)
    @commands.command(name='eval')
    async def _eval(self, ctx, *, body):
        """Evaluates python code"""
        

        env = {
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
            "bot":self.bot,
            "command":ctx.command,

        }

        env.update(globals())

        body = self._cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text) - 1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))

        try:
            to_compile_split = to_compile.split("\n")
            def exec_code():
                exec(to_compile, env)

            if len(to_compile_split) == 2:
                try:
                    await ctx.send(f"`{eval(to_compile_split[1], env)}`")
                except Exception as e:
                    exec_code()
                else:
                    exec_code()
            else:
                exec_code()
            
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')  # tick
        elif err:
            await ctx.message.add_reaction('\u2049')  # x
        else:
            await ctx.message.add_reaction('\u2705')

    def _cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')


    @commands.group()
    async def exa(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Form : `exa` <command>\n__Commands__\n\n`reload`;`shutdown`;`avatar`")

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
        embed.add_field(name="Last launch", value=timedelta(seconds=time.monotonic() - launch))
        embed.add_field(name="Python version", value=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        embed.add_field(name="discord.py version", value=discord.__version__)
        await ctx.send(embed=embed)


def setup(bot):
    owner = Owner(bot)
    owner.exa.add_command(owner.reload)
    owner.exa.add_command(owner.shutdown)
    owner.exa.add_command(owner.stats)

    bot.add_cog(owner)