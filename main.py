import asyncio
import sqlite3
import discord

from discord.ext import commands, tasks
from environs import Env
from itertools import cycle



env = Env()
env.read_env()
token_bot = env("TOKEN")
token = str(token_bot)




custom_prefixes = {}
default_prefix = ['/']

async def _prefix(bot, message):
    if message.guild:
      # sur un serveur, préfix custom
      # cursor.execute("SELECT prefix FROM ABC_prefix WHERE guild_id = ?", (message.guild.id, ))
      # return cursor.fetchone()[0] # ("!", )
      return custom_prefixes.get(message.guild.id, default_prefix)
    else:
      # en MP, préfix par défaut !
      return default_prefix

    
# Initialisation du bot
bot = commands.Bot(command_prefix=_prefix) # 3 shard (0, 1, 2)
bot.remove_command("help")


@bot.command()
@commands.guild_only()
async def setprefix(ctx, *, prefixes):
  # guild_id = ctx.guild.id
  # cursor.execute("SELECT prefix FROM ABC_prefix WHERE guild_id = ?", ctx.guild.id)
  # result = cursor.fetchone()
  #if result is None:
    #cursor.execute("INSERT INTO ABC_prefix VALUES(?, ?)", (guild_id, prefixes))
  #else:
    #cursor.execute("UPDATE ABC_users SET prefix = ? WHERE guild_id = ?", (prefixes, guild_id))
  custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefix # le "or" évite la condition "if not prefix" si le préfix n'est pas renseigné
  await ctx.send("Préfix bien set !")

EMBER_ID = 418154142175854613
ZED_ID = 327074335238127616
OWNER_ID = (EMBER_ID, ZED_ID)


@bot.event
async def on_command_error(ctx, error):
  if ctx.author.id == EMBER_ID:
    await ctx.send(f"```diff\n- {type(error)}\n- {error}```", delete_after=15)
  
  try:
    value = f"**Need more help ?** : `{''.join(await ctx.bot.command_prefix(ctx.bot, ctx.message))}h {ctx.command.name}`"
  except:
    pass
  
  if isinstance(error, commands.errors.MissingPermissions):
    embed = discord.Embed(title=f":x: You don't have the required permissions !", color=0xff0000)
    await ctx.send(embed=embed)
    return # don't send embed help and footer
    
       
  elif isinstance(error, commands.errors.MissingRequiredArgument):
    embed = discord.Embed(color=0xF7754C)
    embed.add_field(name=":x: **Not enough argument**", value=value)
    
  elif isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.BadUnionArgument):
    embed = discord.Embed(color=0xF7754C)
    embed.add_field(name=":x: **Not found | Bad Argument**", value=value)
  else:
    return
  
  await ctx.send(embed=embed)
  #await ctx.send_help(ctx.command)
  
  
# un "iterator" qui revient au début à l'infini sans exception
BOT_ACTIVITY = cycle([" serveurs", " utilisateurs", "V 1.0", "/help", "ZedRoff & Ember"])

@tasks.loop(seconds=5.0)
async def status_loop():
  activity = next(BOT_ACTIVITY)
  if activity == " serveurs":
    activity = str(len(bot.guilds)) + activity
  elif activity == " utilisateurs":
    activity = str(len(bot.users)) + activity
  
  await bot.change_presence(activity=discord.Streaming(name=activity, url="https://twitch.tv/none"))

@bot.event
async def on_ready():
  status_loop.start()


    
if __name__ == "__main__": # SI c'est ce fichier qui est lancé seulement !
  from command.fun.ball8 import ball8
  from command.fun.bingo import bingo
  from command.fun.cat import cat
  from command.fun.dog import dog
  from command.fun.roll import roll

  from command.utils.color import color
  from command.utils.find import find
  from command.utils.lmgtfy import lmgtfy
  from command.utils.ping import ping
  from command.utils.qrcode import qrcode
  from command.utils.say import say
  from command.utils.timer import timer

  from command.information.botinfo import botinfo
  from command.information.serverinfo import serverinfo
  from command.information.userinfo import userinfo

  for command in [ball8, bingo, cat, dog, roll, color, find, lmgtfy, ping, qrcode, say, timer,
                  botinfo, serverinfo, userinfo]:
    bot.add_command(command)

  bot.run(token, reconnect=True)
  
