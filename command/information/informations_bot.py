import time
import discord

from discord.ext import commands
from datetime import datetime

from ..error import CtxEmbed

class BotInformations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner = "ZedRoff & Ember"
        self.support_url = "https://discord.gg/dxHHSqt" # official
        self.invite_bot_url = "https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot"

    @commands.command(aliases=["bot-info"], brief="Bonjour :)")
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot informations", description=f"[Invite me]({self.invite_bot_url.format(self.bot.user.id)})", color=0x0000bf, timestamp=datetime.utcnow())
        embed.add_field(name="➔ Creators", value=self.owner)
        embed.add_field(name="➔ Prefix", value="".join(await ctx.bot.command_prefix(ctx.bot, ctx.message)))
        embed.add_field(name="➔ Name", value=ctx.bot.user)
        embed.add_field(name="➔ Mention", value=ctx.bot.user.mention)
        embed.add_field(name="➔ ID", value=ctx.bot.user.id)
        embed.add_field(name="➔ Servers", value=len(ctx.bot.guilds))
        embed.add_field(name="➔ Users", value=len(ctx.bot.users))
        embed.set_thumbnail(url=ctx.bot.user.avatar)

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):

        start = time.monotonic()
        ping_calc = await ctx.send("...")

        ping_result = round((time.monotonic() - start) * 1000, 3)
        
        latency = round(self.bot.latency * 1000, 3) # round(self.bot.latencies[ctx.guild.shard_id][1] * 1000, 3) with shard

        embed = discord.Embed()
        embed.add_field(name="Latency", value=latency)
        embed.add_field(name="Ping", value=ping_result)

        await ping_calc.edit(content=None, embed=embed)

    @commands.command(aliases=["sup"])
    async def support(self, ctx):

        invite = self.invite_bot_url.format(self.bot.user.id)

        message = f"**__Hello from the support !__ ({self.support_url})**"

        embed = discord.Embed()

        embed.description = f"➔ [CLICK HERE]({self.support_url}) if you want to join support ! \
\n\n➔ [CLICK HERE]({invite}) if you want to invite the bot !"

        embed.set_thumbnail(url="https://lh3.googleusercontent.com/pvhOimTtaDL-1YFGLmMoxa3_aBHEObk9B7VJntEC4lkeqwqNuBYWom7uW8Mb-AzeByU")
        
        await ctx.send(message, embed=embed)

    @commands.command(aliases=["add", "inviteme", "invite-me"]) # in order to have `invite` and `support` in help command
    async def invite(self, ctx):
        await self.support(ctx)

    @commands.command(aliases=["report"], brief="Report a problem with the bot, or suggestion, or ... as you want :D")
    async def feedback(self, ctx, message):
        await self.bot.get_channel(762014696504557581).send(embed=CtxEmbed(ctx, description=message))

    @commands.command()
    async def news(self, ctx):

        embed = discord.Embed(title=f"What's new with {self.bot.user.name} ?")
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/pvhOimTtaDL-1YFGLmMoxa3_aBHEObk9B7VJntEC4lkeqwqNuBYWom7uW8Mb-AzeByU")
        

        embed.description = open(r'C:\Users\Enzo\Documents\PythonProjects\Exarium\command\information\news.txt', 'r').read()

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(BotInformations(bot))