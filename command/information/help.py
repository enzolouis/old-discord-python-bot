import discord

from discord.ext import commands

@commands.command(name="help")
async def help_command(ctx, command=None):
	if command is None:
		embed = discord.Embed(title="List of bot commands", description="`/help <command>` for more informations about the command")
		cmd_cog_no = ["`"+command.name+"`" for command in ctx.bot.commands if command.cog is None]
		cmd_cog_yes = ["`"+command.name+"`" for command in ctx.bot.commands if command.cog is not None]
		cmd_cog_no.sort()
		cmd_cog_yes.sort()
		embed.add_field(name="No cogs", value=", ".join(cmd_cog_no))
		embed.add_field(name="Cogs", value=", ".join(cmd_cog_yes))

		return await ctx.send(embed=embed)

	# if a specific command is called
	command = [cmd for cmd in ctx.bot.commands if cmd.name == command]
	if not command:
		return await ctx.send("This command does not exist")

	command = command[0]
	#cooldown = "".join([str(cooldown[2]) for cooldown in cooldown_cmd if command.name == cooldown[0]]) or "None"
	aliases = "".join(command.aliases) or "None"

	embed = discord.Embed(title=f"{command}'s help page")
	embed.add_field(name="Name", value=command.name)
	embed.add_field(name="Aliases", value=aliases)
	embed.add_field(name="Description", value=command.brief or "None")
	#embed.add_field(name="Cooldown", value=cooldown)
	

	await ctx.send(embed=embed)
