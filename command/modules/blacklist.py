import typing
import sqlite3
import asyncio #non use
import discord

from discord.ext import commands
from python.error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, CtxEmbed



async def owner(ctx):
  return ctx.author.id == 418154142175854613 or ctx.author.id == 327074335238127616 or ctx.author.id == 507753823742459904

 
  
  
  
  
class Blacklist(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.owner = (418154142175854613, 327074335238127616, 507753823742459904)
    self.DB = ".data/data.db"

    
  @commands.group()
  async def blacklist(self, ctx):
      if ctx.invoked_subcommand is None:
        embed = CtxEmbed(ctx, title="Blacklist module", color=0x51ff00,
          description="""The blacklist is a complete system that help you to have a best community !
          **But why ?** The bot's owner look for bad comportement and had the bobby to te blacklist, \
          a lot of reason are possible, like MP pubs, troll, ... And **you** can report these users.\n\n```fix\nAll commands :```""")
        embed.add_field(name="`verif (@user)`", value="verify all users blacklisted in the server (or only one user with the `verif @user`)", inline=False)
        embed.add_field(name="`report [@user] [reason_and_link]`", value="Report an user with evidence (link)", inline=False)
        await ctx.send(embed=embed)


        # only for owner
        if await owner(ctx):
            embed = discord.Embed(title="Blacklist Help page (OWNER)", color=0x51ff00)
            embed.add_field(name="`blacklist-add [@user] [reason_and_link]`", value="Ajouter un utilisateur à la blacklist (merci d'indiquez la raison et la preuve !)", inline=False)
            embed.add_field(name="`blacklist-remove [@user]`", value="Enlever un utilisateur de la blacklist", inline=False)
            await ctx.send(embed=embed)
            
            con = sqlite3.connect(self.DB)
            cursor = con.cursor()

            cursor.execute("SELECT * FROM ABC_blacklist")
            result = cursor.fetchall()
            embed = discord.Embed(title="Blacklist")
            for x in result:
              embed.add_field(name=self.bot.get_user(x[0]), value="**Reason: **"+x[1])
            await ctx.send(embed=embed)
            

  @commands.command()
  @commands.check(owner)
  async def add(self, ctx, user:discord.User, *, evidence): # evidence : reason + link
      try:
          con = sqlite3.connect(self.DB)
          cursor = con.cursor()
          user_id = user.id

          cursor.execute("SELECT * FROM ABC_blacklist WHERE user_id = ?", (user_id, ))
          result = cursor.fetchone()

          if result is None:
              cursor.execute("INSERT INTO ABC_blacklist VALUES(?, ?)", (user_id, evidence))
              await ctx.send(embed=GOOD_USE(f"{user} ajouté à la blacklist avec succès !"))
          else:
              await ctx.send(f"{user} est déja blacklisté !")

      except Exception as e:
          await ctx.send(str(type(e)) + str(e))
          con.rollback()

      else:
          con.commit()
          con.close()
  
  
  
  @commands.command()
  @commands.check(owner)
  async def remove(self, ctx, user:discord.User):
      try:
          con = sqlite3.connect(self.DB)
          cursor = con.cursor()
          user_id = user.id

          cursor.execute("SELECT * FROM ABC_blacklist WHERE user_id = ?", (user_id, ))
          result = cursor.fetchone()

          if result is None:
            await ctx.send(embed=ERROR(f"{user} n'est pas dans la blacklist !"))
          else:
            cursor.execute("DELETE FROM ABC_blacklist WHERE user_id = ?", (user_id, ))
            await ctx.send(embed=GOOD_USE(f"{user} supprimé de la blacklist avec succès !"))

      except Exception as e:
          await ctx.send(str(type(e)) + str(e))
          con.rollback()

      else:
          con.commit()
          con.close()



  @commands.command()
  async def report(self, ctx, member:discord.Member, *, reason):
      await ctx.send("(Attention à bien envoyer la preuve via un lien de preuve !)", delete_after=3)
      embed = discord.Embed(title=f"Report de {ctx.author} ({ctx.author.id})")
      embed.add_field(name="Utilisateur report", value=f"{member} ({member.id})", inline=False)
      embed.add_field(name="Raison", value=reason)
      for x in self.owner:
          owner = self.bot.get_user(x)
          await owner.send(embed=embed)

      await ctx.send("Message envoyé avec succès aux créateurs ! L'utilisateur se verra blacklist ou non.\n **Apercu de votre report :**")
      await ctx.send(embed=embed)


  @commands.command()
  @commands.has_permissions(administrator=True)
  async def verif(self, ctx, member:discord.Member=None):
      try:
          con = sqlite3.connect(self.DB)
          cursor = con.cursor()

          cursor.execute("SELECT user_id, evidence FROM ABC_blacklist") # select *
          result = cursor.fetchall()

          if member is None:
              embed = discord.Embed(title="Users blacklisted on this server", color=0x0000cf)
              for mem in ctx.guild.members:
                  for elt in result:
                      mem_id = elt[0]
                      evidence = elt[1]
                      if mem.id == mem_id: # elt[0] et pas elt car c'est un tuple : [(1328932749, ), (28327483, )]
                          embed.add_field(name=f"**{ctx.guild.get_member(mem_id)}** ({mem_id})", value=f"**Raison** : {evidence}")

              if not embed.fields: # si il n'y a aucun field (aucun blacklisté)
                  embed.description = ":white_check_mark: Your server looks protect.\nNo person in your server is in our blacklist."
              await ctx.send(embed=embed)


          else:
              embed = discord.Embed(title="Test", color=0x0000cf)
              for elt in result:
                  mem_id = elt[0]
                  evidence = elt[1]
                  if member.id == mem_id:
                      embed.add_field(name=f"**{ctx.guild.get_member(mem_id)}** ({mem_id})", value=f"**Raison** : {evidence}")
                      await ctx.send(embed=embed)
                      return

              await ctx.send(embed=ERROR("L'utilisateur n'est pas dans la blacklist"))

      except Exception as e:
          await ctx.send(str(type(e)) + str(e))
          
          

def setup(bot):
  bl = Blacklist(bot)
  bl.blacklist.add_command(bl.verif)
  bl.blacklist.add_command(bl.report)
  bl.blacklist.add_command(bl.add)
  bl.blacklist.add_command(bl.remove)
  bot.add_cog(bl)