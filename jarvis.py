import os
import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# LOAD CHANNEL DATA
def load_channels():
    with open("configs/channels.json") as f:
        return json.load(f)

# PICK RANDOM CHANNEL
def choose_channel():
    data = load_channels()
    channel = random.choice(list(data.keys()))
    return channel, data[channel]

# GENERATE AI TITLE
def generate_topic(niche, country):
    prompt = f"Give ONLY ONE short viral YouTube video title for {niche} in {country}."

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return chat.choices[0].message.content.strip()

# GENERATE AI SCRIPT
def generate_script(topic):
    prompt = f"Write a 30 second viral YouTube Shorts script on: {topic}"

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return chat.choices[0].message.content.strip()

# TELEGRAM HANDLER
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text.lower()

    if user_text == "start":

        channel, info = choose_channel()
        topic = generate_topic(info["niche"], info["country"])

        msg = f"""
🚀 YOUTUBE MISSION

CHANNEL: {channel}
NICHE: {info['niche']}
COUNTRY: {info['country']}
TOPIC: {topic}
"""

        await update.message.reply_text(msg)
        return

    if user_text == "script":

        channel, info = choose_channel()
        topic = generate_topic(info["niche"], info["country"])
        script = generate_script(topic)

        msg = f"""
🎬 AI YOUTUBE SCRIPT

CHANNEL: {channel}
TOPIC: {topic}

{script}
"""

        await update.message.reply_text(msg)
        return

    await update.message.reply_text("Type 👉 start or script")

# BOT START
app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("JARVIS RUNNING 🚀")
app.run_polling()
