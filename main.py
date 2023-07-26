import discord
import discord_slash
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import requests
import json
import os

# Create discord client and slash command client
client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

# Define api url (replace example.com with actual domain name)
api_url = os.getenv('api')

# Define valid types for chat command
valid_types = ["clone", "normal"]

# Create slash command for /help
@slash.slash(name="help", description="Show command usage")
async def help(ctx):
    # Create embed with color blue, title "Command Usage", description of command usage, and footer saying "Made by [REDACTED]"
    embed = discord.Embed(color=discord.Color.blue(), title="Command Usage", description="/help: Show command usage\n/chat [type] [message]: Chat with the bot using a type (clone or normal) and a message")
    embed.set_footer(text="Cool bot made by [REDACTED]")
    # Send embed to context
    await ctx.send(embed=embed)

# Create slash command for /chat
@slash.slash(name="chat", description="Chat with the bot using a type and a message",
    options=[
        create_option(
            name="type",
            description="The type of chatbot (clone or normal)",
            option_type=3,
            required=True
        ),
        create_option(
            name="message",
            description="The message to send to the bot",
            option_type=3,
            required=True
        )
    ]
)
async def chat(ctx, type: str, message: str):
    # Check if type is valid
    if type in valid_types:
        # Get user id from context
        user_id = ctx.author.id
        # Send get request to api url with message, user id, and type as parameters
        response = requests.get(api_url, params={"msg": message, "id": user_id, "mode": type})
        # Parse json response
        data = response.json()
        # Get bot's message from data (assuming it is in the first element of the list)
        bot_message = data[0]["content"]
        # Create embed with title "Bot's Message", description of bot's message, and footer saying "Cool bot made by [REDACTED]"
        embed = discord.Embed(title="Bot's Message", description=bot_message)
        embed.set_footer(text="Cool bot made by [REDACTED]")
        # Send embed to context
        await ctx.send(embed=embed, hidden=True)
    else:
        # Create embed with title "Error" and description saying that user entered wrong type
        embed = discord.Embed(title="Error", description=f"{type} is not a valid type. Please enter clone or normal.")
        # Send embed to context
        await ctx.send(embed=embed)

# Run bot using discord client (replace TOKEN with actual token)
client.run(os.getenv('token'))
