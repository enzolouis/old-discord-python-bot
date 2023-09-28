import discord

from discord.ext import commands

from ..error import CtxEmbed, pag_desc


@commands.command(brief="Find all members with a specific role !")
async def members(ctx, role:discord.Role):
	mem = "\n".join([member.mention for member in role.members])

	embed = CtxEmbed(ctx)

	if not role.members:
		embed.description = f"No member with `{role}` role"
		await ctx.send(embed=embed)
	else:
		await pag_desc(ctx, mem)