import asyncio
import sqlite3
import os
import discord

from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

# load .env file environnment
load_dotenv()

TOKEN = os.environ["TOKEN"]


""" GET PREFIX """
default_prefix = ['/']

async def cmd_prefix(bot, message):
    if message.guild:
      # sur un serveur, préfix custom
      con = sqlite3.connect("data.db")
      cursor = con.cursor()
      cursor.execute("SELECT prefix FROM zel_prefix WHERE prefix_guild_id = ?", (message.guild.id, ))
      prefix = cursor.fetchone() # ("!", )

      return default_prefix if prefix is None else prefix[0]

    else:
      # en MP, préfix par défaut !
      return default_prefix

# Initialize bot
bot = commands.Bot(command_prefix=cmd_prefix)
bot.remove_command("help")

""" PREFIX COMMAND """
@bot.command()
@commands.guild_only()
async def prefix(ctx, prefix=None):
  if prefix is None:
      return await ctx.send(embed=discord.Embed(title=f"Prefix on this server is {bot.command_prefix(bot, ctx.message)}"))
  
  # first argument in case if a user type /prefix "lol d do ifnjef", prefix will be lol
  prefix = prefix.split()[0]
  
  if len(prefix) > 5:
          return await ctx.send(f"Prefix `{prefix}` too big (5 char maximum)")

  con = sqlite3.connect("data.db")
  cursor = con.cursor()
  
  guild_id = ctx.guild.id
  cursor.execute("SELECT prefix FROM zel_prefix WHERE prefix_guild_id = ?", (guild_id, ))
  result = cursor.fetchone()
  
  if result is None:
    cursor.execute("INSERT INTO zel_prefix VALUES(?, ?)", (guild_id, prefix))
  else:
    cursor.execute("UPDATE zel_prefix SET prefix = ? WHERE prefix_guild_id = ?", (prefix, guild_id))
  con.commit()


EMBER_ID = 418154142175854613
ZED_ID = 327074335238127616
OWNER_ID = (EMBER_ID, ZED_ID)



@bot.event
async def on_message(message):
  if message.author.bot or message.channel.__class__ == discord.DMChannel:
    return

  try:
    content = message.content.split()[0]
  except:
    return

  for command in bot.commands:
    command_name = ["!"+command.name] + ["!"+alias for alias in command.aliases]

    if content in command_name:
      con = sqlite3.connect(r"data/data.db")
      cursor = con.cursor()

      cursor.execute("SELECT command_name FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (message.guild.id, command.name))
      result = cursor.fetchone()

      if result is None:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if ctx.author.id == EMBER_ID:
        await ctx.send(f"```diff\n- {type(error)}\n- {error}```", delete_after=15)

    if isinstance(error, commands.errors.CommandNotFound):
        return

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

#@bot.event
async def on_ready():
    status_loop.start()

con = sqlite3.connect(r'data/data.db')
cursor = con.cursor()
print(con, cursor)

@bot.event
async def on_ready():
    global con
    global cursor
    try:
        con = sqlite3.connect(r'data/data.db')
        cursor = con.cursor()
        print(con, cursor)
    except Exception as e:
        print(f'Error {type(e)} while bot try to init db in `on_ready`. --> {e.args}')
    else:
        print('0 error occured in `on_ready`, go go go')


@bot.command()
async def enable(ctx, command_name):
    for command in bot.commands:
        # one case
        if command.name == command_name or command_name in command.aliases:
            con = sqlite3.connect("data/data.db")
            cursor = con.cursor()

            cursor.execute("SELECT command_name FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (ctx.guild.id, command.name))
            result = cursor.fetchone()
            if result is None:
                return await ctx.send("This command is already enable")

            cursor.execute("DELETE FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (ctx.guild.id, command.name))
            con.commit()
            await ctx.send("The command is now enable")

            return

    await ctx.send("This command does not exist.")


@bot.command()
async def disable(ctx, command_name):
    if command_name in ["enable", "disable"]:
        return await ctx.send("You can't disable `disable`, `enable` commands.")

    for command in bot.commands:
        # one case
        if command.name == command_name or command_name in command.aliases:
            con = sqlite3.connect("data/data.db")
            cursor = con.cursor()

            cursor.execute("SELECT command_name FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (ctx.guild.id, command.name))
            result = cursor.fetchone()
            if result is not None:
                return await ctx.send("This command is already disable")

            cursor.execute("INSERT INTO zel_toggle VALUES(?, ?)", (ctx.guild.id, command.name))
            con.commit()
            await ctx.send("The command is now disable")

            return

    await ctx.send("This command does not exist.")



cooldown_cmd = []
def cooldown(command_name, use_before_cooldown, cooldown_duration, **kwargs):
    cooldown_cmd.append((command_name, use_before_cooldown, cooldown_duration))
    return commands.cooldown(use_before_cooldown, cooldown_duration, **kwargs)


if __name__ == "__main__": # SI c'est ce fichier qui est lancé seulement !
    from command.fun.ball8 import ball8
    from command.fun.bingo import bingo
    from command.fun.cat import cat
    from command.fun.dog import dog
    from command.fun.roll import roll

    from command.utils.color import color
    from command.utils.find import find
    from command.utils.lmgtfy import lmgtfy
    from command.utils.qrcode import qrcode
    from command.utils.say import say
    from command.utils.timer import timer

    from command.information.help import help_command

    from command.moderation.ban import ban, unban
    from command.moderation.channel_create import create_channel
    from command.moderation.channel_delete import delete_channel
    from command.moderation.clear import clear
    from command.moderation.kick import kick
    from command.moderation.lock import lock, unlock
    from command.moderation.mute import mute, unmute
    from command.moderation.nickbot import nickbot
    from command.moderation.rename import rename
    from command.moderation.rename_prefix import rename_prefix
    from command.moderation.role_add import addrole
    from command.moderation.role_create import create_role
    from command.moderation.role_delete import delete_role
    from command.moderation.role_remove import removerole
    from command.moderation.slowmode import slowmode

    from command.owner.eval import _eval

    for command in [
        ball8, bingo, cat, dog, roll, 
        color, find, lmgtfy, qrcode, say, timer, help_command, 
        ban, unban, create_channel, delete_channel, clear, kick, lock, unlock, mute, unmute, nickbot, rename,
        rename_prefix, addrole, create_role, delete_role, removerole, slowmode,
        _eval]:
    
        bot.add_command(command)

    extensions = [
        'command.modules.ticket', 'command.modules.warn', 'command.modules.blacklist',
        'command.information.informations', 'command.information.informations_bot'
    ]

    for extension in extensions:
        bot.load_extension(extension)

    bot.run(TOKEN, reconnect=True)