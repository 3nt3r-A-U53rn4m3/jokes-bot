import discord
from dotenv import dotenv_values
from stuff import *
import aiohttp, requests, shutil
#import os

#random test edit

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

@bot.slash_command(description="sends random (hopefully sfw) joke from api")
async def joke(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/joke')
        json = await request.json()
        joke = json['joke']
    await ctx.respond(joke)

@bot.command(description="latency")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.slash_command(description="simp")
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

#https://discord.com/api/oauth2/authorize?client_id=1029476450086158466&permissions=2048&scope=bot