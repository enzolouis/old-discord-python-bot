import discord

from discord.ext import commands

@commands.command(name="help")
async def help_command(ctx, command=None):
	if command is None:
		embed = discord.Embed(title="List of bot commands", description="`/help <command>` for more informations about the command")

		for cog_name, cog in ctx.bot.cogs.items():
			embed.add_field(name=cog_name, value=", ".join([f"`{command}`" for command in cog.get_commands()]), inline=False)
		
		embed.add_field(name="No category", value=", ".join([f"`{command.name}`" for command in ctx.bot.commands if command.cog is None]))


		return await ctx.send(embed=embed)

	# if a specific command is called
	command = [cmd for cmd in ctx.bot.commands if cmd.name == command]
	if not command:
		return await ctx.send("This command does not exist")

	command = command[0]
	aliases = "".join(command.aliases) or "None"

	embed = discord.Embed(title=f"{command}'s help page")
	embed.add_field(name="Name", value=command.name)
	embed.add_field(name="Aliases", value=aliases)
	embed.add_field(name="Description", value=command.brief or "None", inline=False)

	await ctx.send(embed=embed)

	await ctx.send_help(command)