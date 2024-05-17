# READ THE DOCS
# https://discordpy.readthedocs.io/en/stable/ext/commands/index.html

import os
import random
import discord
from dotenv import load_dotenv
from vars import jokes
from discord.ext import commands
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import time

load_dotenv()
# Have to input DISCORD_TOKEN and GUILD_NAME in .env file,
#  which is not uploaded to github
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_NAME = os.getenv("GUILD_NAME")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    # Bot is connected to Discord
    print(f"{bot.user} has connected to Discord")
    guild = discord.utils.get(bot.guilds, name=GUILD_NAME)
    print(f"This Channel is owned by {guild.owner.name}")
    print(f"Connected to '{guild.name}' server id {guild.id}")
    print(f"There are total of {guild.member_count} members")
    print(f"Guild Members:")
    for member in guild.members:
        print(member.name)


@bot.command(name="joke")
async def joke(ctx):
    response = random.choice(jokes)
    await ctx.send(response)


@bot.command(name="calculate")
async def calculate(ctx, expression):
    try:
        result = eval(expression)
        await ctx.send(f"Result: {result}")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command(name="members")
async def members(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD_NAME)
    member_list = [member.name for member in guild.members]
    await ctx.send(f"Members: {member_list}")


@bot.command(name="weather")
async def weather(ctx):
    openmeteo = openmeteo_requests.Client()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 1.2897,
        "longitude": 103.8501,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
        ],
        "timezone": "Asia/Singapore",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_weather_code = current.Variables(3).Value()

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current.Time()))

    output = (
        f"Current time: {current_time}\n"
        + f"Current Temperature: {current_temperature_2m:.1f}°C\n"
        + f"Feels like: {current_apparent_temperature:.1f}°C\n"
        + f"Current Relative Humidity: {current_relative_humidity_2m:.1f}\n"
    )
    weather_code = {
        (0): "Clear sky",
        (1, 2, 3): "Mainly clear, partly cloudy, and overcast",
        (45, 48): "Fog and depositing rime fog",
        (51, 53, 55): "Drizzle: Light, moderate, and dense intensity",
        (56, 57): "Freezing Drizzle: Light and dense intensity",
        (61, 63, 65): "Rain: Slight, moderate and heavy intensity",
        (66, 67): "Freezing Rain: Light and heavy intensity",
        (71, 73, 75): "Snow fall: Slight, moderate, and heavy intensity",
        (77): "Snow grains",
        (80, 81, 82): "Rain showers: Slight, moderate, and violent",
        (85, 86): "Snow showers slight and heavy",
        (95): "Thunderstorm: Slight or moderate",
        (96, 99): "Thunderstorm with slight and heavy hail",
    }
    for key in weather_code:
        if  isinstance(key,tuple) and int(current_weather_code) in key:
            output += f"Weather: {weather_code[key]}"
            break
        else:
            if int(current_weather_code) == key:
                output += f"Weather: {weather_code[key]}"
                break
    await ctx.send(output)

bot.run(TOKEN)
