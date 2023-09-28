import asyncio
import sqlite3
import os
import discord
import aiosqlite

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

        async with aiosqlite.connect(r"data/data.db") as db:
            cursor = await db.execute("SELECT prefix FROM zel_prefix WHERE prefix_guild_id = ?", (message.guild.id, ))
            prefix = await cursor.fetchone() # ("!", )
            prefix = default_prefix if prefix is None else prefix[0]
            await cursor.close()

            return prefix

    else:
        # en MP, préfix par défaut !
        return default_prefix


intents = discord.Intents.all()

# Initialize bot
bot = commands.Bot(command_prefix=cmd_prefix, intents=intents)
bot.remove_command("help")



""" PREFIX COMMAND """
@bot.command()
@commands.guild_only()
async def prefix(ctx, prefix=None):
    if prefix is None:
        return await ctx.send(embed=discord.Embed(title=f"Prefix on this server : {''.join(await bot.command_prefix(bot, ctx.message))}"))

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("Only admin can do that :eyes:")

    # first argument in case if a user type /prefix "lol d do ifnjef", prefix will be lol
    prefix = prefix.split()[0]

    guild_id = ctx.guild.id

    if len(prefix) > 5:
        return await ctx.send(f"Prefix `{prefix}` too big (5 char maximum)")

    async with aiosqlite.connect(r"data/data.db") as db:
        async with db.execute("SELECT prefix FROM zel_prefix WHERE prefix_guild_id = ?", (guild_id, )) as cursor:
            result = await cursor.fetchone()

            try:
                if result is None:
                    await db.execute("INSERT INTO zel_prefix VALUES(?, ?)", (guild_id, prefix))
                else:
                    await db.execute("UPDATE zel_prefix SET prefix = ? WHERE prefix_guild_id = ?", (prefix, guild_id))
            except:
                return await ctx.send("Error while set new prefix...")
            else:
                await db.commit()

            await ctx.send(f"Set new prefix : `{prefix}`")


EMBER_ID = 418154142175854613
ZED_ID = 327074335238127616
DODUO_ID = 684117553974345730
OWNER_ID = (EMBER_ID, ZED_ID)


@bot.event
async def on_message(message):
    print("message:", message.content)
    if message.author.bot or message.channel.__class__ == discord.DMChannel:
        return

    if message.content in (f"<@{bot.user.id}>", f"<@!{bot.user.id}>"):
        return await message.channel.send(embed=discord.Embed(color=0xfffffc, description=f"Hey user ! My prefix is `{''.join(await bot.command_prefix(bot, message))}`"))

    if not len(message.content.split()) > 0: # not possible but check
        print("test")
        return
    print(message.content)

    content = message.content.split()[0]
    
    try:
        pref = "".join(await bot.command_prefix(bot, message))
    except Exception as e:
        print(e, type(e))

    for command in bot.commands:
        command_name = [pref+command.name] + [pref+alias for alias in command.aliases]
        if content in command_name:
            print("1...", end="\r")
            async with aiosqlite.connect(r"data/data.db") as db:
                async with db.execute("SELECT command_name FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (message.guild.id, command.name)) as cursor:
                    print("2...", end="\r")
                    result = await cursor.fetchone()
                    print("3...", end="\r")
                    print(result or "Rien.......")
                    if result is None:
                        print("4 - END.")
                        return await bot.process_commands(message)
    print("not found")


async def send_error(ctx, message, color=0xff0000):
    help_ = f"{''.join(await bot.command_prefix(bot, ctx.message))}help {ctx.command.name} for more informations"
    embed = discord.Embed(title=message, color=color)
    embed.set_footer(text=help_)

    try:
        await ctx.send(embed=embed)
    except: # if not perm send_link :
        try:
            await ctx.send(f"> {message}\n\n**{help_}**")
        except: # if not perm send_messages, bruh
            pass

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(type(error))

    error = getattr(error, "original", error)

    await ctx.send(f"```fix\n{type(error)}\n```")

    if ctx.author.id == EMBER_ID or ctx.author.id == DODUO_ID:
        await ctx.send(f"```diff\n- {type(error)}\n- {error}```", delete_after=15)

    if isinstance(error, commands.errors.CommandNotFound):
        return

    elif isinstance(error, commands.errors.MissingPermissions):
        await send_error(ctx, f":x: You don't have the required permissions  : {' ; '.join(error.missing_perms)}", color=0xff0000)

    elif isinstance(error, discord.Forbidden):
        await send_error(ctx, ":x: There is a problem with my permissions, I can't do that. To be usefull with all commands, I need administrator permissions.", color=0xff0000)
   
    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        await send_error(ctx, f"There is a cooldown of {int(error.cooldown.per)} seconds ! Wait {round(error.retry_after)} seconds")

    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await send_error(ctx, f":x: **Not enough argument**. Argument missing : {error.param}", color=0xF7754C)
      
    elif isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.BadUnionArgument):
        await send_error(ctx, ":x: **Not found | Bad Argument**", color=0xF7754C)
    else:
        return

  
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
    if command_name in ("enable", "disable"):
        return await ctx.send("You can't disable/enable `disable`, `enable` commands.")

    for command in bot.commands:
        # one case
        if command.name == command_name or command_name in command.aliases:
            async with aiosqlite.connect("data/data.db") as db:
                cursor = await db.execute("SELECT command_name FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (ctx.guild.id, command.name))
                result = await cursor.fetchone()
                if result is None:
                    return await ctx.send("This command is already enable")

                await db.execute("DELETE FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (ctx.guild.id, command.name))
                await db.commit()
                await cursor.close()

                return await ctx.send("The command is now enable")

    await ctx.send("This command does not exist.")


@bot.command()
async def disable(ctx, command_name):
    if command_name in ("enable", "disable"):
        return await ctx.send("You can't disable/enable `disable`, `enable` commands.")

    for command in bot.commands:
        # one case
        if command.name == command_name or command_name in command.aliases:
            async with aiosqlite.connect("data/data.db") as db:
                cursor = await db.execute("SELECT command_name FROM zel_toggle WHERE guild_id = ? AND command_name = ?", (ctx.guild.id, command.name))
                result = await cursor.fetchone()
                if result is not None:
                    return await ctx.send("This command is already disable")

                await db.execute("INSERT INTO zel_toggle VALUES(?, ?)", (ctx.guild.id, command.name))
                await db.commit()
                await cursor.close()

                return await ctx.send("The command is now disable")

    await ctx.send("This command does not exist.")



cooldown_cmd = []
def cooldown(command_name, use_before_cooldown, cooldown_duration, **kwargs):
    cooldown_cmd.append((command_name, use_before_cooldown, cooldown_duration))
    return commands.cooldown(use_before_cooldown, cooldown_duration, **kwargs)



async def main():
    from command.utils.color import color, rgb, hexa
    from command.utils.find import find
    from command.utils.members import members
    from command.utils.poll import poll
    from command.utils.lmgtfy import lmgtfy
    from command.utils.qrcode import qrcode
    from command.utils.timer import timer
    from command.utils.length import length, lengthword
    from command.utils.hastebin import hastebin
    from command.utils.b64cmd import b64encode, b64decode

    from command.information.help import help_command

    from command.moderation.nickbot import nickbot
    from command.moderation.rename import rename
    from command.moderation.rename_prefix import rename_prefix
    from command.moderation.role_add import addrole
    from command.moderation.role_create import create_role
    from command.moderation.role_delete import delete_role
    from command.moderation.role_remove import removerole
    from command.moderation.slowmode import slowmode
    from command.betacommand.listbeta import list_

    for command in [
        list_,
        color, find, lmgtfy, qrcode, timer, help_command, length, lengthword, hastebin, b64encode, b64decode, rgb, hexa, poll, members,
        nickbot, rename, rename_prefix, addrole, create_role, delete_role, removerole, slowmode,]:
    
        bot.add_command(command)

    extensions = [
        'command.fun.fun',
        'command.modules.ticket', 'command.modules.warn', 'command.modules.blacklist',
        'command.information.informations', 'command.information.informations_bot', 'command.owner', 'command.moderation.basics'
    ]

    for extension in extensions:
        await bot.load_extension(extension)

    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__": # only this file
    asyncio.run(main())
