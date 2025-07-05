import discord
import feedparser
import asyncio
import json
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

POSTED_ENTRIES = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await ensure_channels_exist()
    check_feeds.start()

async def ensure_channels_exist():
    with open("feeds.json") as f:
        feeds = json.load(f)

    for guild in bot.guilds:
        category = discord.utils.get(guild.categories, name="Game News")
        if not category:
            category = await guild.create_category("Game News")

        for game in feeds:
            channel_name = game.lower().replace(" ", "-")
            if not discord.utils.get(category.channels, name=channel_name):
                await guild.create_text_channel(channel_name, category=category)

@tasks.loop(minutes=10)
async def check_feeds():
    with open("feeds.json") as f:
        feeds = json.load(f)

    for guild in bot.guilds:
        category = discord.utils.get(guild.categories, name="Game News")
        if not category:
            continue

        for game, url in feeds.items():
            channel_name = game.lower().replace(" ", "-")
            channel = discord.utils.get(category.channels, name=channel_name)
            if not channel:
                continue

            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                entry_id = entry.get("id", entry.get("link"))
                if entry_id not in POSTED_ENTRIES:
                    embed = discord.Embed(
                        title=entry.title,
                        description=entry.summary[:200] + "...",
                        url=entry.link,
                        color=discord.Color.blurple()
                    )
                    embed.set_footer(text=game)
                    await channel.send(embed=embed)
                    POSTED_ENTRIES.add(entry_id)

import os
bot.run(os.getenv("YOUR_BOT_TOKEN"))
