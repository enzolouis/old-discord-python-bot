import typing
import asyncio
import sqlite3
import discord

from discord.ext import commands
from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, CtxEmbed




class Warn(commands.Cog):
  
  
  def __init__(self, bot, con, cursor):
    self.bot = bot
    self.con = con
    self.cursor = cursor
    #self.DB = r'C:\Users\Enzo\Documents\PythonProjects\Exarium\data\data.db'
    
  
  # function to check if author role <= member.role
  @staticmethod
  async def check_role(ctx, member, punishments):
    if ctx.author.top_role.position <= member.top_role.position:
      await ctx.send(embed=ERROR_PUNISHMENTS(punishments))
      return False
    else:
      return True
  
  @commands.has_permissions(administrator=True)
  @commands.command(name="warn-config")
  async def warn_config(self, ctx):
    await ctx.send("""Okay, let's process to warn's system configuration !
**You have to do choice a positive integer number, how many warn a user need to have to take sanctions
*Help : put "0" if you don't want that the user take the sanctions.***
Let's go !""")
    
    def check(message):
      return message.author == ctx.author and message.content.isdigit()
    
    try:
      await ctx.send("Send number of warn in order to allow bot mute the member (for 12 hours)")
      mute_warn = await self.bot.wait_for("message", check=check, timeout=60)
      await ctx.send("Send number of warn in order to allow bot kick the member")
      kick_warn = await self.bot.wait_for("message", check=check, timeout=60)
      await ctx.send("Send number of warn in order to allow bot ban the member (for all life)")
      ban_warn = await self.bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
      await ctx.send("To late, please restart the command.")
    else:
      
      await ctx.send("Well done !", delete_after=2)
      
      
      guild_id = ctx.guild.id
      mute_warn = int(mute_warn.content)
      kick_warn = int(kick_warn.content)
      ban_warn = int(ban_warn.content)
      
      embed = discord.Embed(title="Configuration")
      embed.add_field(name="Warn number to mute 24 hours", value=mute_warn)
      embed.add_field(name="Warn number to kick", value=kick_warn)
      embed.add_field(name="Warn number to ban 7 days", value=ban_warn)
      
      await ctx.send(embed=embed)
      
      self.cursor.execute("SELECT * FROM ABC_sanctions_warn")
      self.cursor.execute("SELECT * FROM ABC_sanctions_warn WHERE guild_id = ?", (guild_id, ))
      
      result = self.cursor.fetchone()
      if result is None:
        self.cursor.execute("INSERT INTO ABC_sanctions_warn VALUES(?, ?, ?, ?)", (guild_id, mute_warn, kick_warn, ban_warn))
      else:
        self.cursor.execute("UPDATE ABC_sanctions_warn SET mute = ?, kick = ?, ban = ? WHERE guild_id = ?", (mute_warn, kick_warn, ban_warn, guild_id))
      self.con.commit()

      
  @commands.has_permissions(manage_messages=True)
  @commands.command()
  async def warn(self, ctx, member:discord.Member, *, reason="Aucune raison"):
      if not await Warn.check_role(ctx, member, "warn"): return
      
      try:
          user_id = member.id
          guild_id = ctx.guild.id

          self.cursor.execute("SELECT * FROM ABC_warn WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
          result = self.cursor.fetchone()
          
          # ajouter les warns
          if result is None:
              self.cursor.execute("INSERT INTO ABC_warn VALUES(?, ?, ?, ?, ?, ?)", (guild_id, user_id, 1, 0, 0, 0)) # ajouter un premier warn
          else:
              self.cursor.execute("UPDATE ABC_warn SET warn = ? WHERE guild_id = ? AND user_id = ?", (result[2]+1, guild_id, user_id)) # ajouter d'autre warn

          # requête pour trouver le nombre de warn nécessaire au mute/kick/ban
          self.cursor.execute("SELECT mute, kick, ban FROM ABC_sanctions_warn WHERE guild_id = ?", (guild_id, ))
          result_sanctions = self.cursor.fetchone()
          # requête pour trouver le nombre de warn de l'utlisateur. Et son nombre de mute/kick/ban provoqué par le nombre de warn
          self.cursor.execute("SELECT warn, mute_with_warn, kick_with_warn, ban_with_warn FROM ABC_warn WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
          result_number = self.cursor.fetchone()
          
          embed = GOOD_USE(f"L'utilisateur {member} a été warn ! :information_source: `warn-help`", color=0xffc900)
          
          # si le /warn-config a bien été configuré
          if result_sanctions is not None:
            warn_to_be_mute = result_sanctions[0]
            warn_to_be_kick = result_sanctions[1]
            warn_to_be_ban = result_sanctions[2]
            
            warn_total = result_number[0]
            mute_number = result_number[1]
            kick_number = result_number[2]
            ban_number = result_number[3]
            
            
            # warn_to_be_... != 0 : veut dire si pendant le /warn-config l'owner n'a pas choisi 0, 0 veut dire la sanction n'aura jamais lieu
            # warn_total = warn_to_be_... : veut dire, si on attend le nombre de warn configuré dans /warn-config, alors il est sanctionné (mute, ...)
            
            if warn_total == warn_to_be_ban and warn_to_be_ban != 0:
              try: await member.ban(reason=f"{warn_total} Warn")
              except: pass
              else:
                embed.add_field(name=f"{warn_to_be_ban} warn", value="Ban")
                self.cursor.execute("UPDATE ABC_warn SET ban_with_warn = ? WHERE guild_id = ? AND user_id = ?", (ban_number+1, guild_id, user_id))

            elif warn_total == warn_to_be_kick and warn_to_be_kick != 0:
              try: await member.kick(reason=f"{warn_total} Warn")
              except: pass
              else:
                embed.add_field(name=f"{warn_to_be_kick} warn", value="Kick")
                self.cursor.execute("UPDATE ABC_warn SET kick_with_warn = ? WHERE guild_id = ? AND user_id = ?", (kick_number+1, guild_id, user_id))
                
            elif warn_total == warn_to_be_mute and warn_to_be_mute != 0:
              for x in ctx.guild.text_channels:
                if x.permissions_for(member).send_messages:
                  await x.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages=False, read_messages=x.permissions_for(member).read_messages))

              
              embed.add_field(name=f"{warn_to_be_mute} warn", value="Mute for 12 hours")
              await ctx.send(embed=embed)
              
              self.cursor.execute("UPDATE ABC_warn SET mute_with_warn = ? WHERE guild_id = ? AND user_id = ?", (mute_number+1, guild_id, user_id))
              self.con.commit() # commit ici pour pas attendre la fin du mute pour commit...
              #self.con.close() # close ici sinon le sleep va bloqué l'accès a la db
              
              await asyncio.sleep(43200) # 12 hours
              
              for x in ctx.guild.text_channels:
                if not x.permissions_for(member).send_messages:
                  await x.set_permissions(member, overwrite=None)


              return # return pour pas continuer et re .close et re .commit et ré envoyer l'embed
                  
          
          # dans tous les cas
          await ctx.send(embed=embed)
          
      except Exception as e:
          self.con.rollback()

      else:
          self.con.commit()

  @commands.has_permissions(manage_messages=True)
  @commands.command()
  async def unwarn(self, ctx, member:discord.Member):
      if not await Warn.check_role(ctx, member, "unwarn"): return
    
      try:
          user_id = member.id
          guild_id = ctx.guild.id

          self.cursor.execute("SELECT * FROM ABC_warn WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
          result = self.cursor.fetchone()

          if result is None: # si user pas inscrit dans la bdd ou si il n'a aucun warn (<= pour verif)
              await ctx.send(embed=discord.Embed(title=f"{member} n'a aucun warn !"))
              return
          else:
              if result[2] == 1: # si il a 1 warn et qu'on fait cette commande /unwarn, il est suppr de la db
                  self.cursor.execute("SELECT * FROM ABC_warn WHERE user_id = ? AND warn = ?", (user_id, 1))
                  self.cursor.execute("DELETE FROM ABC_warn WHERE user_id = ? AND warn = ?", (user_id, 1)) # a corriger

              else:
                  self.cursor.execute("UPDATE ABC_warn SET warn = ? WHERE guild_id = ? AND user_id = ?", (result[2]-1, guild_id, user_id))


          await ctx.send(embed=GOOD_USE(f"L'utilisateur {member} a été unwarn ! :information_source: `warn-help`", color=0xffc900))


      except Exception as e:
          self.con.rollback()

      else:
          self.con.commit()
  
  @commands.has_permissions(administrator=True)
  @commands.command(name="warn-clear", aliases=["clear-warn"])
  async def clear_warn(self, ctx):
    # test
    try:
      guild_id = ctx.guild.id

      self.cursor.execute("SELECT * FROM ABC_warn WHERE guild_id = ?", (guild_id, ))
      result = self.cursor.fetchone() or await ctx.send(embed=ERROR(f"Aucun warn n'a été donné sur le serveur !"))

      self.cursor.execute("DELETE FROM ABC_warn WHERE guild_id = ?", (guild_id, ))
      
      await ctx.send(embed=GOOD_USE("Il n'y a plus aucun warn sur le serveur"))


    except Exception as e:
      await ctx.send(str(type(e)) + str(e))
      self.con.rollback()

    else:
      self.con.commit()
    


  @commands.has_permissions(manage_messages=True)
  @commands.command()
  async def warns(self, ctx, member:discord.Member):
      user_id = member.id
      guild_id = ctx.guild.id

      self.cursor.execute("SELECT * FROM ABC_warn WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
      result = self.cursor.fetchone()

      if result is None: # si il n'est pas dans la bdd
          # simulation de la bdd
          embed=discord.Embed(title=f"Warn de {ctx.guild.get_member(member.id)} ({member.id})")
          embed.add_field(name="WARNS", value="0", inline=False)
          embed.add_field(name="Mute with warn", value="0", inline=False)
          embed.add_field(name="Kick with warn", value="0", inline=False)
          embed.add_field(name="Ban with warn", value="0", inline=False)
          
      else:
          embed = discord.Embed(title=f"Warn de {ctx.guild.get_member(result[1])} ({result[1]})")
          embed.add_field(name="WARNS", value=result[2], inline=False)
          embed.add_field(name="Mute with warn", value=result[3], inline=False)
          embed.add_field(name="Kick with warn", value=result[4], inline=False)
          embed.add_field(name="Ban with warn", value=result[5], inline=False)

      await ctx.send(embed=embed)


  @commands.command(name="warn-list")
  async def checkallwarn(self, ctx):
      try:
          guild_id = ctx.guild.id

          self.cursor.execute("SELECT user_id, warn FROM ABC_warn WHERE guild_id = ?", (guild_id, ))
          result = self.cursor.fetchall()
          # example : [('Ember#3398', 418154142175854613, 1), ('ZedRoff#6268', 327074335238127616, 4)]


          embed = discord.Embed(title=f"Warns totals")
          for member in result:
              embed.add_field(name=self.bot.get_user(member[0]), value=f"Warns : {member[1]}")
          if not embed.fields:
              embed.description = ":white_check_mark: Aucun utilisateur n'a de warn sur le serveur."

          await ctx.send(embed=embed)

      except Exception as e:
          print(str(type(e)) + str(e))
          self.con.rollback()
  

async def setup(bot):
    from ..cmd_main import con, cursor
    await bot.add_cog(Warn(bot, con, cursor))