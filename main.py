import discord
from dotenv import dotenv_values
from stuff import *
import aiohttp, requests, shutil
import os

DISCORD_TOKEN = dotenv_values(".env")["DISCORD_TOKEN"]

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if basicStrip(message.content).startswith("im") or basicStrip(message.content).startswith("i'm"):
      user = getContent(basicStrip(message.content))
      await message.channel.send(message.author.mention + " Hi**{}**, I'm dad!".format(user))

    await bot.process_commands(message)

@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command()
async def joke(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/joke')
        json = await request.json()
        joke = json['joke']
    await ctx.respond(joke)

@bot.slash_command()
async def simp(ctx, avatar=""):
  await ctx.send("Generating SIMP card...")
  #await ctx.trigger_typing() 

  if avatar == "":
    avatar = ctx.author.avatar.url
  
  r = requests.get('https://some-random-api.ml/canvas/simpcard', data={'avatar': avatar}, stream=True)
  
  with open('simp.png', 'wb') as lolsimp:
    shutil.copyfileobj(r.raw, lolsimp)
  
  await ctx.respond(file=discord.File("simp.png"))

bot.run(DISCORD_TOKEN)