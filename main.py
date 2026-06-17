import os
import discord
from google import genai
from google.genai import types
from flask import Flask
from threading import Thread

# 1. Web Loophole Server
app = Flask('')

@app.route('/')
def home():
    return "Bot is awake and running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 2. Discord Configuration
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

gemini_client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

BOT_INSTRUCTIONS = """
You are a cool, helpful Discord chatbot powered by Gemini.
- Keep your replies short and friendly.
- Match the casual tone of a Discord user.
"""

@discord_client.event
async def on_ready():
    print(f"Bot is live in the cloud as {discord_client.user}!")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.content,
            config=types.GenerateContentConfig(
                system_instruction=BOT_INSTRUCTIONS,
                max_output_tokens=300
            )
        )
        await message.channel.send(response.text)
    except Exception as e:
        print(f"Error: {e}")

# 3. Launch Services
keep_alive()
discord_client.run(DISCORD_TOKEN)
"""

@discord_client.event
async def on_ready():
    print(f"Bot is live in the cloud as {discord_client.user}!")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.content,
            config=types.GenerateContentConfig(
                system_instruction=BOT_INSTRUCTIONS,
                max_output_tokens=300,
            ),
        )
        await message.channel.send(response.text)
    except Exception as e:
        print(f"Error: {e}")

# 3. LAUNCH BOTH SERVICES TOGETHER
keep_alive()
discord_client.run(DISCORD_TOKEN)
                max_output_tokens=300,
            ),
        )
        await message.channel.send(response.text)
    except Exception as e:
        print(f"Error: {e}")

discord_client.run(DISCORD_TOKEN)
