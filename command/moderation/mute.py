import discord

from discord.ext import commands

from ..error import GOOD_USE, ERROR_PERMISSIONS_BOT, ERROR_PUNISHMENTS, ERROR, WARNING, CtxEmbed


@commands.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member:discord.Member, *, reason="Aucune raison"):
  muted = discord.utils.get(ctx.guild.roles, name="muted") or discord.utils.get(ctx.guild.roles, name="Muted")
  already_muted = discord.utils.get(member.roles, name="muted") or discord.utils.get(member.roles, name="Muted")
  
  if already_muted is not None:
    await ctx.send(embed=ERROR(f"User {member} is already muted"))
    return
  
  if muted is None:
    def check(message):
      return message.content == "oui" and message.author == ctx.author
    
    await ctx.send("Voulez-vous créer le rôle \"muted\" ? Aucun rôle \"muted\" détécté sur le serveur.\n **Répondez \"oui\" si vous le voulez.**")
    await ctx.bot.wait_for("message", check=check)
    permissions = discord.Permissions()
    permissions.send_messages = False
    muted = await ctx.guild.create_role(name="muted", permissions=permissions)
    """for x in ctx.guild.channels:
      await ctx."""

    await ctx.send(f"Le rôle {muted.mention} a été créé. **Placez ce rôle plus haut que les membres pour qu'il soit utile.**")
    
    return
  
  if ctx.author.top_role.position <= member.top_role.position:
    await ctx.send(embed=ERROR_PUNISHMENTS("mute"))
  else:
    try:
      await member.add_roles(muted, reason=reason)
    except discord.errors.Forbidden:
      await ctx.send(embed=ERROR_PERMISSIONS_BOT())
    else:
      await ctx.send(embed=GOOD_USE(f"{member.name} ({member.id}) a été rendu muet.\n Raison : *{reason}*"))



@commands.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member:discord.Member, *, reason="Aucune raison"):
  if ctx.author.top_role.position <= member.top_role.position:
    await ctx.send(embed=ERROR_PUNISHMENTS("unmute"))
    return
  
  muted = discord.utils.get(member.roles, name="muted") or discord.utils.get(member.roles, name="Muted")
  if muted is not None:
    try:
      await member.remove_roles(muted, reason=reason)
    except discord.errors.Forbidden:
      await ctx.send(embed=ERROR_PERMISSIONS_BOT())
    else:
      await ctx.send(embed=GOOD_USE(f"{member.name} ({member.id}) n'est désormais plus muet.\n Raison : *{reason}*"))
  
  else:
    await ctx.send(embed=ERROR(f"{member.name} n'est pas muet !"))
  
