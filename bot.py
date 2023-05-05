import discord
import random
import time

intents = discord.Intents.all()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is online and connected to Discord!")
    print(f"Bot user ID: {client.user.id}")

@client.event
async def on_message(message):
    content = message.content.strip()

    print(f"Message received ({len(content)} chars): {content}")

    if content.startswith("!roll "):
        args = content[6:].split("d")
        if len(args) == 2 and args[0].isdigit() and args[1].isdigit():
            num_dice = int(args[0])
            dice_sides = int(args[1])
        elif len(args) == 1 and args[0].isdigit():
            num_dice = 1
            dice_sides = int(args[0])
        else:
            return

        seed = time.time()
        random.seed(seed)

        rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
        rolls_str = ", ".join(str(r) for r in rolls)
        total = sum(rolls)
        response = f"{message.author.mention}\n**Result: {num_dice}d{dice_sides} ({rolls_str})**\n**Total: {total}**\nSeed: {seed}"
        await message.channel.send(response)


client.run('Your Token Here')