import asyncio
import discord

from discord.ext import commands
from random import randint


@commands.command()
async def bingo(ctx, maximum:int=100):
  if maximum < 1:
    await ctx.send("**Veuillez entrer un nombre entier positif !**")
    return
  
  random_nbr = randint(1, maximum)
  await ctx.send(embed=GOOD_USE(f"Bingo from 1 to {maximum} !"))
  
  def check(message):
    if message.content.isdigit():
      return int(message.content) == random_nbr and message.channel == ctx.channel
  
  try:
    msg = await ctx.bot.wait_for('message', check=check, timeout=300)
  except asyncio.TimeoutError:
    return await ctx.send(f"Tout le monde a perdu ! Le numéro à trouver était **{random_nbr}**")
  await ctx.send(f"Le joueur {msg.author.mention} a gagné ! Le numéro à trouver était **{random_nbr}**")
  
  
@commands.command()
async def breakbingo(ctx, maximum:int=100):
  if maximum < 1:
    await ctx.send("**Veuillez entrer un nombre entier positif !**")
    return
  
  random_nbr = randint(1, maximum)
  await ctx.send(embed=GOOD_USE(f"Juste prix infini entre 1 et {maximum} !"))
  
  
  def check(message):
    return message.channel == ctx.channel and (message.content.isdigit() or message.content in ["stop", "break", "cancel"])
  
  while True:
      try:
        bingo = await ctx.bot.wait_for("message", check=check, timeout=50)
        await ctx.send("pass")
        if bingo.content in ["stop", "break", "cancel"]:
          if bingo.author == ctx.author:
            return await ctx.send(f"Fin du jeu forcé. Le numéro à trouver était **{random_nbr}**")
          else:
            await ctx.send("Vous ne pouvez pas arrêter le jeu.")
            continue
          
        bingo_content = int(bingo.content)
        if random_nbr == bingo_content:
          return await ctx.send(f"Le joueur {bingo.author.mention} a gagné ! Le numéro à trouver était **{random_nbr}**")
        await ctx.send(f"{bingo.author.name} : " + (":arrow_up:" if random_nbr > int(bingo.content) else ":arrow_down:"))
      
      except asyncio.TimeoutError:
        return await ctx.send(f"Tout le monde a perdu ! Le numéro à trouver était **{random_nbr}**")