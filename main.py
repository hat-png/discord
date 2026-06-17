import os
import discord
from google import genai
from google.genai import types
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

gemini_client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
DISCORD_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

BOT_INSTRUCTIONS = "You are a cool, helpful Discord chatbot powered by Gemini. Keep replies short."

@discord_client.event
async def on_ready():
    print("Bot is online!")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.content,
            config=types.GenerateContentConfig(
                system_instruction=BOT_INSTRUCTIONS
            )
        )
        await message.channel.send(response.text)
    except Exception as e:
        print(f"Error: {e}")

keep_alive()
discord_client.run(DISCORD_TOKEN)
