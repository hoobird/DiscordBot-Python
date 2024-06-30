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

    current_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(current.Time()))

    output = (
        f"Current time: {current_time}\n"
        + f"Current Temperature: {current_temperature_2m:.1f}°C\n"
        + f"Feels like: {current_apparent_temperature:.1f}°C\n"
        + f"Current Relative Humidity: {current_relative_humidity_2m:.1f}\n"
    )
    weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight intensity",
    81: "Rain showers: Moderate intensity",
    82: "Rain showers: Violent intensity",
    85: "Snow showers: Slight intensity",
    86: "Snow showers: Heavy intensity",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
    }

    output += f"Weather: {weather_codes[int(current_weather_code)]}"
    await ctx.send(output)

bot.run(TOKEN)
