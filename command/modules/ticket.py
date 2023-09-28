import asyncio
import sqlite3
import typing
import discord

from discord.ext import commands
from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed

class Ticket(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.DB = r'C:\Users\Enzo\Documents\PythonProjects\Exarium\data\data.db'
  
  
  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
    delete_log = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete).get()
      
    con = sqlite3.connect(self.DB)
    cursor = con.cursor()
    cursor.execute("SELECT user_id, channel_id, subject FROM ABC_ticket_new WHERE channel_id = ?", (channel.id, ))
    result = cursor.fetchone()
    
    if result is not None:
      # logs
      await self.log(channel, delete_log.user, "close", "Delete manuel")
      
      cursor.execute("DELETE FROM ABC_ticket_new WHERE channel_id = ?", (result[1], ))
      con.commit()

      
  async def log(self, channel, author, mode, target, **kwargs):
    try:
      
      con = sqlite3.connect(self.DB)
      cursor = con.cursor()
      cursor.execute("SELECT log_channel_id FROM ABC_config_ticket WHERE guild_id = ?", (channel.guild.id, ))
      ticket_config = cursor.fetchone()
      
      log_id = ticket_config[0]
      
      
      log_channel = self.bot.get_channel(ticket_config[0]) # get_channel(id)
      if log_channel is None:
        return

      cursor.execute("SELECT user_id, channel_id, subject FROM ABC_ticket_new WHERE channel_id = ?", (channel.id, ))
      result = cursor.fetchone()
      

      if log_id != 0:
        config = []
        if mode == "create": config.extend(("Opened", 0x58FA82, kwargs['for_member']))
        elif mode == "close": config.extend(("Closed", 0xDB1702, f"➔ Closed because : {target[:1000]}"))
        #elif mode == "rename": config.extend(("Renamed", 0x00c2cc, f"➔ Old name : {kwargs['oldname']}\n➔ New name : {target}"))
        elif mode == "remove": config.extend(("Member removed", 0xcc7122, f"➔ Member removed : {kwargs['member']}"))
        elif mode == "admin": config.extend(("Only administrator", 0xcc7122, ""))
        elif mode == "clear": config.extend(("All cleared", 0xDB1702, ""))
        else: return
        
        
        by = f"➔ {config[0]} by : {author}" if not mode  == "create" else ""

        embed = discord.Embed(title=f"Ticket : {config[0]}", color=config[1])
        if mode == "clear":
          embed.description = f"➔ All tickets cleared by {author}"
        
        else:
          embed.description = f"""
➔ Subject : {target[:1000] if mode == "create" else result[2]} ...
➔ Generate by : {author if mode == "create" else channel.guild.get_member(result[0])}
{by}
{config[2]}
"""
        await log_channel.send(embed=embed)
        
    except Exception as e:
      await channel.send(e)
    else:
      con.close()
      
  @commands.group()
  async def ticket(self, ctx):
    
    con = sqlite3.connect(self.DB)
    cursor = con.cursor()
    
    cursor.execute("SELECT category_id FROM ABC_config_ticket WHERE guild_id = ?", (ctx.guild.id, ))
    ticket_config = cursor.fetchone()
    
    if ctx.invoked_subcommand is None:
      embed = CtxEmbed(ctx, title="Ticket module")
      embed.add_field(name="`ticket config (edit)` (ADMIN)", value="See ticket system configuration or edit if `ticket config edit`")
      embed.add_field(name="`ticket open (subject)`", value="Open a new ticket")
      embed.add_field(name="`ticket open (@user) (subject)` (manage channels permissions)", value="Open a new ticket to a member")
      embed.add_field(name="`ticket close (reason)`(ADMIN)", value="Close a ticket")
      embed.add_field(name="`ticket admin`(ADMIN)", value="Change ticket permissions to only admin")
      embed.add_field(name="`ticket remove [@user]` (manage channels permissions)", value="Remove a member from a ticket")
      embed.add_field(name="`ticket clear (reason)` (ADMIN)", value="Clear all ticket channel from the server")
      await ctx.send(embed=embed)
    
    elif ctx.invoked_subcommand is not None and ticket_config is not None:
      cursor.execute("SELECT user_id, channel_id, subject FROM ABC_ticket_new WHERE channel_id = ?", (ctx.channel.id, ))
      result = cursor.fetchone()
      
      if result is None and ctx.invoked_subcommand not in [self.create, self.config, self.clear]:
          await ctx.send(embed=ERROR("Vous n'êtes pas dans un salon de ticket"))
          raise Exception
    
    
    if ticket_config is None and ctx.invoked_subcommand is not self.config: # si la requête WHERE guild_id = ? renvoit None
      await ctx.send(embed=ERROR("Le système de ticket n'est pas configuré. Les commandes du système de ticket(sauf celle-ci) ne peut pas être tapé.\n`ticket config edit` pour configurer le système."))
      raise Exception
    
    
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def config(self, ctx, mode=None): # mode : edit | other...
    con = sqlite3.connect(self.DB)
    cursor = con.cursor()
    
    guild_id = ctx.guild.id
    cursor.execute("SELECT category_id, log_channel_id FROM ABC_config_ticket WHERE guild_id = ?", (guild_id, ))
    result = cursor.fetchone()
    
    if mode == "edit":
      # catch the category
      await ctx.send("**Entrez une catégorie ! (avec son nom ou son ID)**")
      await ctx.send(f"Apercu de la liste des catgories :```fix\n{' - '.join([category.name for category in ctx.guild.categories]) if ctx.guild.categories else 'No category...'}```")
      def check(message):
        content = message.content.lower()
        categories = [x.name.lower() for x in ctx.guild.categories]
        categories_id = [str(x.id) for x in ctx.guild.categories]

        return content in categories or content in categories_id

      try:
        category = await self.bot.wait_for("message", check=check, timeout=60)
        category = await commands.CategoryChannelConverter().convert(ctx, category.content)
        category_id = category.id
      except asyncio.TimeoutError:
        return await ctx.send("Vous avez mis trop de temps...")

      # -----------------------------------------------------------------------------------------------------------------------------------------------------------
      # catch the log channel
      await ctx.send("**Entrez le salon ou les logs des tickets se feront ! \"no\" si vous ne voulez pas de salon de logs**")

      def check(message):
        content = message.content.lower()
        channels = [x.name.lower() for x in ctx.guild.text_channels]
        channels_id = [str(x.id) for x in ctx.guild.text_channels]
        channels_mention = [f"<#{x.id}>" for x in ctx.guild.text_channels] # the channel's mention format

        return content in channels or content in channels_id or content in channels_mention or content == "no"

      try:
        log_channel = await self.bot.wait_for("message", check=check, timeout=60)
        log_channel_id = 0 if log_channel.content == "no" else (await commands.TextChannelConverter().convert(ctx, log_channel.content)).id

      except asyncio.TimeoutError:
        return await ctx.send("Vous avez mis trop de temps...")
      
      # register in database
      
      try:
        if result is None:
          cursor.execute("INSERT INTO ABC_config_ticket VALUES(?, ?, ?)", (guild_id, category_id, log_channel_id))
        else:
          cursor.execute("UPDATE ABC_config_ticket SET category_id = ?, log_channel_id = ? WHERE guild_id = ?", (category_id, log_channel_id, guild_id))

        await ctx.send(embed=GOOD_USE(f"""La catégorie pour les tickets est désormais :\n**{ctx.guild.get_channel(category_id)} ({category_id})**
        \nSalon de log : {ctx.guild.get_channel(log_channel_id) if  log_channel_id != 0 else "Aucun"}"""))

    
      except Exception as e:
        con.rollback()
      else:
        con.commit()

    elif mode == "remove":
      if result is None:
        return await ctx.send(embed=ERROR("Ticket module is not already configured"))
      cursor.execute("DELETE FROM ABC_config_ticket WHERE guild_id = ?", (guild_id, ))
      con.commit()
      await ctx.send(embed=GOOD_USE("Ticket module is now not configured"))
    
    else:
      # dans tous les autres cas, on peut seulement voir la configuration sans edit
      if result is not None:
        embed = CtxEmbed(ctx, title="Ticket system configuration")
        embed.add_field(name="Catégorie ou les tickets s'ajoute", value=self.bot.get_channel(result[0]))
        embed.add_field(name="Salon de logs pour les tickets", value=self.bot.get_channel(result[1]) or "None")
        await ctx.send(embed=embed)
      else:
        await ctx.send(embed=WARNING("Le système de ticket n'est pas configuré."))
      
      await ctx.send("`ticket config edit` si vous voulez modifier cette configuration")
  
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def clear(self, ctx, *, reason="No reason"):
    con = sqlite3.connect(self.DB)
    cursor = con.cursor()
    
    cursor.execute("SELECT channel_id FROM ABC_ticket_new WHERE guild_id = ?", (ctx.guild.id, ))
    result = cursor.fetchall()
    # don't need to catch if result is None cause of fetchall() that return an empty list if request is null
    
    if not result:
      return await ctx.send(embed=WARNING("Aucun salons ticket n'a été trouvé"))
    
    for channels_id in result:
      channel = ctx.guild.get_channel(channels_id[0])
      if channel is not None:
        await channel.delete()
    
    # delete all tickets from database
    cursor.execute("DELETE FROM ABC_ticket_new WHERE guild_id = ?", (ctx.guild.id, ))
    con.commit()
    
    await ctx.send(embed=GOOD_USE("All ticket has been removed from your guild !"))
    await self.log(ctx.channel, ctx.author, "clear", reason)
      
  @commands.command(aliases=["open", "new"])
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def create(self, ctx, member:typing.Optional[discord.Member]=None, *, target="No reason"):
    
    
    if member is not None and not ctx.author.guild_permissions.manage_channels:
      return await ctx.send(f"Vous n'avez pas les permissions de créer un ticket à {member.name}")
    
    con = sqlite3.connect(self.DB)
    cursor = con.cursor()
    
    guild_id = ctx.guild.id
    user_id = ctx.author.id
    channel_id = ctx.channel.id
    
    cursor.execute("SELECT category_id FROM ABC_config_ticket WHERE guild_id = ?", (guild_id, ))
    ticket_config = cursor.fetchone() # 0 risque de None, car le /ticket (commands.group()) est appelé avant et vérifie si ca ne vaut pas None

    category = ctx.guild.get_channel(ticket_config[0])

    if category is None: # if category has been deleted
      return await ctx.send(embed=ERROR("Ticket module is not configured"))
    
    
    user_ticket = member or ctx.author
    
    
    close_command = "".join(await self.bot.command_prefix(self.bot, ctx.message)) + "ticket close"
    
    overwrites = {
      ctx.guild.default_role:discord.PermissionOverwrite(read_messages=False),
      ctx.guild.me:discord.PermissionOverwrite(read_messages=True, send_messages=True),
      user_ticket:discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
    # pas besoin d'autoriser l'invocateur de la commande si il a fait /ticket @user car c'est forcément quelqu'un avec manage_channels qui a fait la commande
    # et les rôles avec manage_channels sont mis dans le ticket (voir boucle ci dessous)
    for role in ctx.guild.roles:
      if role.permissions.manage_messages or role.permissions.manage_channels or role.permissions.manage_roles:
        overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
    try:
      new_channel = await ctx.guild.create_text_channel(str(user_ticket), category=category, overwrites=overwrites)
    except:
      return await ctx.send(embed=ERROR("I don't have the required permissions to create the channel."))
    embed=WARNING(f"{user_ticket.mention}\nNew ticket open\n`{close_command}`(admin) pour fermer le ticket.")
    embed.add_field(name="Author", value=f"{ctx.author}\n({ctx.author.id})")
    await ctx.channel.send(f"Your ticket has been create : {new_channel.mention}")
    await new_channel.send(embed=embed)
    await new_channel.send(f">>> {target}")
    try:
      cursor.execute("INSERT INTO ABC_ticket_new VALUES(?, ?, ?, ?)", (guild_id, user_id, new_channel.id, target[:1000])) # target : subject
    except:
      con.rollback()
    else:
      con.commit()
      await self.log(ctx.channel, ctx.author, "create", target, for_member="" if member is None else f"➔ Generate for : {user_ticket}")
  
  @commands.has_permissions(manage_channels=True)
  @commands.command(aliases=["close"])
  async def delete(self, ctx, *, target="Rien"):
    con = sqlite3.connect(self.DB)
    cursor = con.cursor()
    
    guild_id = ctx.guild.id
    user_id = ctx.author.id
    channel_id = ctx.channel.id
    
    cursor.execute("SELECT user_id, channel_id, subject FROM ABC_ticket_new WHERE channel_id = ?", (channel_id, ))
    result = cursor.fetchone()
    
    cursor.execute("SELECT category_id FROM ABC_config_ticket WHERE guild_id = ?", (guild_id, ))
    ticket_config = cursor.fetchone()
    
    await ctx.send(embed=GOOD_USE("Fermeture du ticket ..."))

    await asyncio.sleep(3)
    await self.log(ctx.channel, ctx.author, "close", target)

    cursor.execute("DELETE FROM ABC_ticket_new WHERE channel_id = ?", (result[1], ))
    con.commit()

    # delete channel
    await ctx.channel.delete()
    
  @commands.has_permissions(manage_permissions=True)
  @commands.command(aliases=["remove-user"]) # aliases
  async def remove(self, ctx, member:discord.Member):
    
    if member.permissions_in(ctx.channel).administrator:
      return await ctx.send("**Enlever un membre avec la permission administrateur ne fera rien**")

    await ctx.channel.set_permissions(member, overwrite=discord.PermissionOverwrite(read_messages=False))

    await self.log(ctx.channel, ctx.author, "remove", "lol", member=str(member))

    
  @commands.has_permissions(administrator=True)
  @commands.command(aliases=["adminonly", "ao", "onlyadmin"]) # aliases
  async def admin(self, ctx, *, target="Rien"):
    
    con = sqlite3.connect(self.DB)
    cursor = con.cursor()
    cursor.execute("SELECT user_id, channel_id, subject FROM ABC_ticket_new WHERE channel_id = ?", (ctx.channel.id, ))
    result = cursor.fetchone()
    
    # only admin, the bot and the ticket author
    overwrites = {
      ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
      ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
      ctx.guild.get_member(result[0]):discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
    await ctx.channel.edit(overwrites=overwrites)
    await self.log(ctx.channel, ctx.author, "admin", target)
          
  
  

async def setup(bot):
  tick = Ticket(bot)
  tick.ticket.add_command(tick.config)
  tick.ticket.add_command(tick.create)
  tick.ticket.add_command(tick.delete)
  tick.ticket.add_command(tick.remove)
  tick.ticket.add_command(tick.admin)
  tick.ticket.add_command(tick.clear)
  await bot.add_cog(tick)