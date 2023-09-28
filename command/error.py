import discord
import asyncio

from datetime import datetime
from .emojis import arrow

"""
- remplacer les discord.Embed par CtxEmbed (en précisant ctx en paramètre)
- enlever tous les set_footer (déja par défaut dans CtxEmbed)
- enlever tous les timestamp= (pareil)
- remplacer set_thumbnail par thumbnail= pour chaque embed
"""


class CtxEmbed(discord.Embed): # an embed to set timestamp and footer and a default color (blue)
  def __init__(self, ctx, color=0x009eff, **kwargs):
    discord.Embed.__init__(self, color=color, timestamp=datetime.utcnow(), **kwargs)
    self.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar)


def GOOD_USE(formula, color=0x2eff00):
  embed = discord.Embed(description=formula, color=color)
  embed.set_thumbnail(url="https://cdn.glitch.com/5f373f55-ab8d-4671-80ea-c21805f80314%2Fcheck.png?v=1591744869882")
  return embed


def ERROR_PERMISSIONS_BOT():
  embed = discord.Embed(description=f":x: I don't have the required permissions !", color=0xff0000)
  return embed

def ERROR_PUNISHMENTS(type_punishments):
  embed = discord.Embed(description=f":x: You can't {type_punishments} this user !", color=0xff0000)
  return embed

def ERROR(content):
  embed = discord.Embed(description=":x: " + content, color=0xDB1702)
  return embed

def WARNING(content):
  embed = discord.Embed(description=":warning: " + content, color=0xffc900)
  embed.set_thumbnail(url="https://cdn.glitch.com/5f373f55-ab8d-4671-80ea-c21805f80314%2Fwarninganimated.gif?v=1590491532002")
  return embed

def is_positive_integer(integer:str) -> bool:
    try:
        number = int(integer)
    except:
        return False
    else:
        return number > 0


def format_hours(arg):
    if arg.isdigit():
        arg += "s"

    raw_durat = arg

    type_durat = arg[-1]
    durat = arg[:-1]

    if not durat.isdigit() or type_durat not in ("s", "m", "h"):
        return None

    durat = int(durat)

    if type_durat == "m":
        raw_durat = f"{durat} minutes"
        durat *= 60
    elif type_durat == "h":
        raw_durat = f"{durat} hours"
        durat*=3600
    elif type_durat == "s":
        raw_durat = f"{durat} seconds"

    return durat, raw_durat


def paginate(text):
    last = 0
    pages = []
    for curr in range(0, len(text)):
        # si curr est égal à 0, 1980, 1980 *2, 1980 * 3, etc
        if curr % 1980 == 0:
            pages.append(text[last:curr])
            last = curr


    # ajouter la dernière occurence, le dernier élément, qui n'est jamais ajouté dans le if !
    pages.append(text[last:curr+1])
    
    return list(filter(lambda a: a != '', pages)) # delete the first element that is '' (obligatory) because range(0, ..) and 0 % 1980 == 0


async def pag_desc(ctx, description, **kwargs):
    if len(description) < 2040: # 2048 : max char of an embed description, so 2040 is good
        return await ctx.send(embed=CtxEmbed(ctx, description=description))

    arrows = (arrow["left"], arrow["right"])

    desc = paginate(description)
    page_number = 0
    page_max = len(desc)


    embed = CtxEmbed(ctx, description=desc[0])

    #embed.set_footer(text=kwargs.get("footer"), icon_url=kwargs.get("footer_icon_url"))

    message = await ctx.send(embed=embed)

    await message.add_reaction(arrows[0])
    await message.add_reaction(arrows[1])


    def check(reaction, user):
        return reaction.message.channel == message.channel and user == ctx.author and str(reaction.emoji) in arrows

    while True:
        try:
            react, user = await ctx.bot.wait_for("reaction_add", check=check, timeout=60)
        except asyncio.TimeoutError:
            break

        await message.remove_reaction(react.emoji, user)
        await message.remove_reaction(react.emoji, user)

        if str(react.emoji) == arrow["right"] and page_max > page_number + 1:
            embed.description = desc[page_number + 1]
            page_number+=1

            await message.edit(embed=embed)

        elif str(react.emoji) == arrow["left"] and page_number > 0:
            print("LEFT")
            embed.description = desc[page_number - 1]
            page_number-=1

            await message.edit(embed=embed)

    await message.clear_reactions()
