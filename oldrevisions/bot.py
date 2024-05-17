# READ THE DOCS
# https://discordpy.readthedocs.io/en/stable/api.html

import os
import random
import discord
from dotenv import load_dotenv
from vars import jokes

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_NAME = os.getenv("GUILD_NAME")

intents = discord.Intents.default()
intents.members = True
intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # Bot is connected to Discord
    print(f"{client.user} has connected to Discord")
    guild = discord.utils.get(client.guilds, name= GUILD_NAME)
    print(f"This Channel is owned by {guild.owner}")
    print(f"Connected to '{guild.name}' server id {guild.id}")
    print(f"There are total of {guild.member_count} members")
    print(f"Guild Members:")
    for member in guild.members:
        print(member.name)

@client.event
async def on_member_join(member):
    # When a new member joins the server
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord Server!")

@client.event
async def on_message(message):
    # When a message is sent in the server
    
    # Preventing the bot from replying to itself
    if message.author == client.user:
        return
    
    # if the message has the word "joke"
    if "joke" in message.content.lower():
        response = random.choice(jokes)
        await message.channel.send(response)

    if message.content.startswith("calculate"):
        expression=message.content[len("calculate"):].strip()
        try:
            result = eval(expression)
            await message.channel.send(f"Result: {result}")
        except Exception as e:
            await message.channel.send(f"Error: {e}")

    
client.run(TOKEN)