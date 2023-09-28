import discord

from discord.ext import commands
from datetime import datetime

from ..error import CtxEmbed


class Informations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="id")
    async def id_(self, ctx, user:discord.User=None):
        user = user or ctx.author
        await ctx.send(embed=CtxEmbed(ctx, description=user.id))


    @commands.command()
    async def avatar(self, ctx, member:discord.Member=None):

        member = member or ctx.author

        # str() convert url object in text, see docs
        embed = CtxEmbed(ctx, url=str(member.avatar), title=f"{member.name}'s avatar url")
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)


    @commands.command(aliases=["user-info"])
    async def userinfo(self, ctx, member:discord.Member=None):
        member = member or ctx.author
          
        roles = "\n".join([x.name for x in member.roles[1:]])[:1020]

        embed = CtxEmbed(ctx, title=f"{member}'s informations")
        embed.add_field(name="➔ Name", value=member.name)
        embed.add_field(name="➔ Mention", value=member.mention)
        embed.add_field(name="➔ ID", value=member.id)
        create = member.created_at.strftime('%A, %d %B %Y | %I:%M%p')
        embed.add_field(name="➔ Account creation", value=create)
        embed.add_field(name="➔ Activity", value=member.activity)
        embed.add_field(name="➔ Status", value=member.status)
        join = member.joined_at.strftime('%A, %d %B %Y | %I:%M%p')
        embed.add_field(name="➔ Server join", value=join)
        embed.add_field(name="➔ Higher role", value=member.top_role.name)
        embed.add_field(name="➔ Roles", value=" - ".join(roles.split("\n")[:-1]))
        embed.set_thumbnail(url=member.avatar)
        await ctx.send(embed=embed)



    @commands.command(aliases=["server-info"])
    @commands.guild_only()
    async def serverinfo(self, ctx):  
        embed = CtxEmbed(ctx, title="Server informations")  
        embed.add_field(name="➔ Name", value=ctx.guild.name)
        embed.add_field(name="➔ ID", value=ctx.guild.id)
        create = ctx.guild.created_at.strftime('%A, %d %B %Y | %I:%M%p')
        embed.add_field(name="➔ Creation", value=create)
        embed.add_field(name="➔ Member count", value=ctx.guild.member_count) # len(ctx.guild.members)
        embed.add_field(name="➔ Owner", value=ctx.guild.owner)
        embed.add_field(name="➔ Channels", value=len(ctx.guild.channels))
        embed.add_field(name="➔ Roles", value=len(ctx.guild.roles))
        embed.add_field(name="➔ Emojis", value=len(ctx.guild.emojis))
        embed.add_field(name="➔ Region", value=ctx.guild.region)
        embed.add_field(name="➔ AFK channel", value=ctx.guild.afk_channel if ctx.guild.afk_channel else "Aucun")
        nsfw = [x for x in ctx.guild.text_channels if x.is_nsfw()]
        embed.add_field(name="➔ NSFW channels", value=len(nsfw) if nsfw else "Aucun")

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)



    @commands.command(aliases=["role-info"], brief="Bonjour :)")
    async def roleinfo(self, ctx, role:discord.Role):

        if role.is_default():
            name = "everyone"
        else:
            name = role.name

        embed = CtxEmbed(ctx, title="Role informations")
        embed.add_field(name="➔ Name", value=name)
        embed.add_field(name="➔ ID", value=role.id)
        if not role.is_default(): # not utils to mention @everyone role, and role.mention with everyone role do : @@everyone
            embed.add_field(name="➔ Mention", value=role.mention)
        embed.add_field(name="➔ Creation", value=role.created_at.strftime('%A, %d %B %Y | %I:%M%p'))
        embed.add_field(name="➔ Mentionable ?", value=role.mentionable)
        embed.add_field(name="➔ Separated from other ?", value=role.hoist)
        embed.add_field(name="➔ Position", value=role.position)
        embed.add_field(name="➔ Color", value=role.color or "None")

        await ctx.send(embed=embed)



    @commands.command(aliases=["channel-info"], brief="Bonjour :)")
    async def channelinfo(self, ctx, channel:discord.TextChannel=None):
        channel = channel or ctx.channel

        embed = CtxEmbed(ctx, title="Channel informations")
        embed.add_field(name="➔ Category", value=channel.category)
        embed.add_field(name="➔ Name", value=channel.name)
        embed.add_field(name="➔ ID", value=channel.id)
        embed.add_field(name="➔ Mention", value=channel.mention)
        embed.add_field(name="➔ Creation", value=channel.created_at.strftime('%A, %d %B %Y | %I:%M%p'))
        embed.add_field(name="➔ Slowmode", value=channel.slowmode_delay or "off")
        embed.add_field(name="➔ NSFW ?", value=channel.nsfw)
        embed.add_field(name="➔ Topic", value=channel.topic or "None")

        await ctx.send(embed=embed)



    @commands.command(aliases=["emoji-info"])
    async def emojiinfo(self, ctx, emoji:discord.Emoji):
      embed = CtxEmbed(ctx, title="Emoji informations")
      embed.add_field(name="➔ Guild", value=emoji.guild)
      embed.add_field(name="➔ Name", value=emoji.name)
      embed.add_field(name="➔ ID", value=emoji.id)
      create = emoji.created_at.strftime('%A, %d %B %Y | %I:%M%p')
      embed.add_field(name="➔ Creation", value=create)
      embed.add_field(name="➔ Animated ?", value=emoji.animated)
      embed.add_field(name="➔ Urls", value=emoji.url)
      embed.set_thumbnail(url=emoji.url)
      
      await ctx.send(embed=embed)



    @commands.command(aliases=["invite-info"])
    async def inviteinfo(self, ctx, invite:discord.Invite):
        embed = CtxEmbed(ctx, title="Invite informations")
        embed.add_field(name="➔ Guild", value=invite.guild)
        embed.add_field(name="➔ Channel", value=invite.channel)
        embed.add_field(name="➔ Inviter", value=invite.inviter)
        embed.add_field(name="➔ Code", value=invite.code) # invite.code == invite.id
        embed.add_field(name="➔ URL", value=invite.url)
        embed.add_field(name="➔ Max age", value=invite.max_age)
        embed.add_field(name="➔ Max uses", value=invite.max_uses)

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Informations(bot))