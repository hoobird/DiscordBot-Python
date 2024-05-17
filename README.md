# Discord Bot README

Welcome to my Discord Bot! This guide will help you understand the bot's functionality, how to use its commands, and provide examples for better understanding.

## Project Description
This Discord Bot is designed to enhance your Discord server with a variety of useful and fun commands. From telling jokes to performing calculations, listing members, and providing current weather information, this bot aims to add a layer of interaction and utility to your server.

## Commands and Usage

| Command / Usage       | Description                                        |
|----------------|----------------------------------------------------|
| `!joke`        | Sends a random joke from a predefined list.        |
| `!calculate <expression>`  | Evaluates a mathematical expression.               |
| `!members`     | Lists all members of the guild.                    |      
| `!weather`     | Provides current weather information for a predefined location. (Uses open-meteo free weather api) |            

## Examples

### Using `!joke`
```sh
User: !joke
Bot: Why don't scientists trust atoms? Because they make up everything!
```

### Using `!calculate`
```sh
User: !calculate 5 * (3 + 2)
Bot: Result: 25
```

### Using `!members`
```sh
User: !members
Bot: Members: ['Alice', 'Bob', 'Charlie']
```

### Using `!weather`
```sh
User: !weather
Bot: 
Current time: 2023-05-17 14:05:32
Current Temperature: 30.5°C
Feels like: 32.1°C
Current Relative Humidity: 70.5%
Weather: Mainly clear, partly cloudy, and overcast
```

## Running the Bot
To run the bot, execute the following command in your terminal:
```sh
python discordbot.py
```
You should see output indicating that the bot has connected to Discord and the specified guild.
