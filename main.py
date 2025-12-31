import discord
import asyncio
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os

load_dotenv("token.env")

USER_ID = 970019137923465297
CHANNEL_ID = 1057362972718157914

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_state = None

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN variable is not set")

def status_category(status: discord.Status):
    return status in (discord.Status.online, discord.Status.dnd)

async def send_commands(channel, is_online):
    if is_online:
        await channel.send("?stop")

        await asyncio.sleep(10)
        await channel.send("?close Roblox")
    else:
        await channel.send("?start")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await check_presence(initial=True)
    presence_check.start()

async def check_presence():
    global last_state

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        return

    for guild in bot.guilds:
        member = guild.get_member(USER_ID)
        if member:
            current_state = status_category(member.status)

            print(f"Discord status: {member.status}, category: {current_state}")

            if last_state is None:
                last_state = current_state
                await send_commands(channel, current_state)
                return

            if current_state != last_state:
                last_state = current_state
                await send_commands(channel, current_state)

            return

@tasks.loop(seconds=10)
async def presence_check():
    await check_presence()

bot.run(TOKEN)