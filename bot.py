import discord
import random
import time
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix=":", intents=intents)

@client.event
async def on_ready():
    print("Bot is online and connected to Discord!")
    print(f"Bot user ID: {client.user.id}")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return

    await client.process_commands(message)

@client.command()
async def roll(ctx, *, roll_string):
    content = roll_string.strip()
    print(f"Message received ({len(content)} chars): {content}")

    if content.startswith("d"):
        args = content.split("d")
        if len(args) == 2 and args[0] == "" and args[1].isdigit():
            num_dice = 1
            dice_sides = int(args[1])
        else:
            return
    else:
        args = content.split("d")
        if len(args) == 2 and args[0].isdigit() and args[1].isdigit():
            num_dice = int(args[0])
            dice_sides = int(args[1])
        else:
            return

    seed = time.time()
    random.seed(seed)

    rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
    rolls_str = ", ".join(str(r) for r in rolls)
    total = sum(rolls)
    response = f"{ctx.author.mention}\n**Result: {num_dice}d{dice_sides} ({rolls_str})**\n**Total: {total}**\nSeed: {seed}"

    # Delete the command message if the roll is successful
    if rolls:
        await ctx.message.delete()

    await ctx.send(response)

client.run('Your Token Here')