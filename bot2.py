# READ THE DOCS
# https://discordpy.readthedocs.io/en/stable/ext/commands/index.html

import os
import random
import discord
from dotenv import load_dotenv
from vars import jokes
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_NAME = os.getenv("GUILD_NAME")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Bot is connected to Discord
    print(f"{bot.user} has connected to Discord")
    guild = discord.utils.get(bot.guilds, name= GUILD_NAME)
    print(f"This Channel is owned by {guild.owner.name}")
    print(f"Connected to '{guild.name}' server id {guild.id}")
    print(f"There are total of {guild.member_count} members")
    print(f"Guild Members:")
    for member in guild.members:
        print(member.name)

@bot.command(name='joke')
async def joke(ctx):
    response = random.choice(jokes)
    await ctx.send(response)

@bot.command(name='calculate')
async def calculate(ctx, expression):
    try:
        result = eval(expression)
        await ctx.send(f"Result: {result}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(TOKEN)