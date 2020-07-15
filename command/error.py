import discord
from datetime import datetime

"""
- remplacer les discord.Embed par CtxEmbed (en précisant ctx en paramètre)
- enlever tous les set_footer (déja par défaut dans CtxEmbed)
- enlever tous les timestamp= (pareil)
- remplacer set_thumbnail par thumbnail= pour chaque embed
"""


class CtxEmbed(discord.Embed): # an embed to set timestamp and footer and a default color (blue)
  def __init__(self, ctx, color=0x009eff, **kwargs):
    discord.Embed.__init__(self, color=color, timestamp=datetime.utcnow(), **kwargs)
    self.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)


def GOOD_USE(formula, color=0x2eff00):
  embed = discord.Embed(description=formula, color=color)
  embed.set_thumbnail(url="https://cdn.glitch.com/5f373f55-ab8d-4671-80ea-c21805f80314%2Fcheck.png?v=1591744869882")
  return embed


def ERROR_PERMISSIONS_BOT():
  embed = discord.Embed(description=f":x: Je n'ai pas les permissions nécessaire !", color=0xff0000)
  return embed

def ERROR_PUNISHMENTS(type_punishments):
  embed = discord.Embed(description=f":x: Vous ne pouvez pas {type_punishments} cette personne !", color=0xff0000)
  return embed

def ERROR(content):
  embed = discord.Embed(description=":x: " + content, color=0xDB1702)
  return embed

def WARNING(content):
  embed = discord.Embed(description=":warning: " + content, color=0xffc900)
  embed.set_thumbnail(url="https://cdn.glitch.com/5f373f55-ab8d-4671-80ea-c21805f80314%2Fwarninganimated.gif?v=1590491532002")
  return embed