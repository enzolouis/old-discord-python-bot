import asyncio
import discord

from discord.ext import commands
from pytio import Tio, TioRequest

from .. import emojis

from ..error import format_hours

tio = Tio()

@commands.command()
async def run(ctx, langage, *, code):
    request = TioRequest(lang=langage, code=code)
    response = tio.send(request)
    await ctx.send(response.result or "0 result")




@commands.command(brief="""Create a nice poll with some configuration, as mode, duration.\n\n
:small_blue_diamond: `poll mode duration "title" "choices"`
`duration` : `12h`,`15m`, `5h`, `10s`, `5s`, `infinity`, `12`(=`12s`), `0`(=`infinity`)

`normal` mode -> Poll with {emojis.number[0]}, {emojis.number[1]}, {emojis.number[2]}, ... reaction until 26
Minimum : `poll normal 10s "title" "choice 1"`
Maximum : `poll normal 2h "title" "choice 1" "choice 2" "choice 3" "choice 4" ...` until 26 choices !

`simple` mode -> Poll with {emojis.truefalse["true"]}, {emojis.truefalse["false"]} and {emojis.truefalse["noyes"]}
Minimum : `poll simple 15m "title"`
Maximum : `poll simple infinity "title" "right sentence" "wrong sentence" "noyes sentence"`""")

async def poll(ctx, mode:str, durat:str, *args): # infos ; nbr de réactions max : 20 (faire des dictm 11->26)
        if mode not in ("normal", "simple"):
            mode = "normal"

        if durat == "infinity" or durat == "0":
            durat = raw_durat = "infinity"
        else:
            durat = format_hours(durat)
            if durat is None:
                return await ctx.send("Please enter a good duration like : `30s`, `1h`, `10m` or `infinity`")
            durat, raw_durat = durat

        if len("".join(args)) > 1500:
            return await ctx.send("Max args size for poll is 1500.")
        if len(args[0]) > 255:
            return await ctx.send("Max title size for poll is 256.")

        title = args[0]
        choices = args[1:]

        # variable de l'embed du sondage
        poll = discord.Embed(title=title, color=0x0000bf)
        poll.set_footer(text=f"Poll by {ctx.author} - Duration : {raw_durat}", icon_url=ctx.author.avatar)

        if mode == "normal":
            if len(choices) < 1:
                await ctx.send(f"Poll with `normal` mode bad", delete_after=5)
                return await ctx.send(embed=embed_help_sondage())

            #poll.description = "".join([f"{emojis.number[int(elt)]} {choices[elt]}\n" for elt in range(len(choices))])
            desc_list = [f"{emojis.number[elt]} {choices[elt]}" for elt in range(len(choices))]

            poll.description = "\n".join(desc_list)
            
            poll_msg = await ctx.send(embed=poll)

            reacts = []
            for react in emojis.number: # réduire : for react in reactions :...number[react]
                reacts.append(react)
                if len(reacts) > len(choices) : break # sinon un while (moins opti) / >= ?
                await poll_msg.add_reaction(react) # dictionnaire / "key"s

        elif mode == "simple":
            reacts = [emojis.truefalse["true"], emojis.truefalse["false"], emojis.truefalse["noyes"]]
            choice1 = "" if len(choices) == 0 else choices[0]
            choice2 = "" if len(choices) <= 1 else choices[1]
            choice3 = "" if len(choices) <= 2 else choices[2]

            desc_list = [f"{reacts[0]} {choice1}", f"{reacts[1]} {choice2}", f"{reacts[2]} {choice3}"]

            poll.description = "\n\n".join(desc_list)

            poll_msg = await ctx.send(embed=poll)
            await poll_msg.add_reaction(emojis.truefalse["true"])
            await poll_msg.add_reaction(emojis.truefalse["false"])
            await poll_msg.add_reaction(emojis.truefalse["noyes"])

        if durat == "infinity":
            return

        await asyncio.sleep(durat)
 
        embed_result = discord.Embed(title=poll.title, color=poll.color)
        desc = []
        count = 0
        for react in (await ctx.channel.fetch_message(poll_msg.id)).reactions:
            if str(react.emoji) in reacts:
                desc.append(f"{desc_list[count]}\n→ {react.count - 1} votes")
                count+=1

        embed_result.description = "\n\n".join(desc)
        embed_result.set_footer(text=f"Poll ended by {ctx.author} - Duration : {raw_durat}", icon_url=ctx.author.avatar)
        await poll_msg.edit(embed=embed_result)
        await poll_msg.clear_reactions()
        

def embed_help_sondage():
            return discord.Embed(title="Help page (poll)", description=f""":small_blue_diamond: `poll mode duration "title" "choices"`
`duration` : `12h`,`15m`, `5h`, `10s`, `5s`, `infinity`, `12`(=`12s`), `0`(=`infinity`)

`normal` mode -> Poll with {emojis.number[0]}, {emojis.number[1]}, {emojis.number[2]}, ... reaction until 26
Minimum : `poll normal 10s "title" "choice 1"`
Maximum : `poll normal 2h "title" "choice 1" "choice 2" "choice 3" "choice 4" ...` until 26 choices !

`simple` mode -> Poll with {emojis.truefalse["true"]}, {emojis.truefalse["false"]} and {emojis.truefalse["noyes"]}
Minimum : `poll simple 15m "title"`
Maximum : `poll simple infinity "title" "right sentence" "wrong sentence" "noyes sentence"`
""")


@poll.error
async def sondage_error(ctx, error):
    error = getattr(error, "original", error)
    if isinstance(error, commands.errors.InvalidEndOfQuotedStringError) or isinstance(error, commands.errors.ExpectedClosingQuoteError):
        await ctx.send("Bad format... Please make sure your quote \" are valid.")
    await ctx.send(embed=embed_help_sondage())