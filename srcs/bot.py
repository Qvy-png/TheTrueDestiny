import discord
import random
import time
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.messages = True

class CustomHelpCommand(commands.DefaultHelpCommand):
    # Override the methods to modify the help command behavior

    # Example: Modify the help command's title
    def get_command_signature(self, command):
        return f"**Command:** {self.clean_prefix}{command.qualified_name}"

client = commands.Bot(command_prefix=":", intents=intents, help_command=None)

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

    # Split the roll_string into parts by the '+' symbol
    parts = content.split('+')

    # Handle the dice roll part
    roll_part = parts[0].strip()
    if roll_part.startswith("d"):
        args = roll_part.split("d")
        if len(args) == 2 and args[0] == "" and args[1].isdigit():
            num_dice = 1
            dice_sides = int(args[1])
        else:
            return
    else:
        args = roll_part.split("d")
        if len(args) == 2 and args[0].isdigit() and args[1].isdigit():
            num_dice = int(args[0])
            dice_sides = int(args[1])
        else:
            return

    # Handle the rolls
    seed = time.time()
    random.seed(seed)

    rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
    rolls_str = f"{', '.join(str(r) for r in rolls)}"
    total_rolls = sum(rolls)

    # Handle the additional numbers
    additional_numbers = []
    if len(parts) > 1:
        for additional_part in parts[1:]:
            additional_part = additional_part.strip()
            if additional_part.isdigit():
                additional_numbers.append(int(additional_part))
            else:
                return

    total_additional = sum(additional_numbers)
    total = total_rolls + total_additional

    rolls_result = f"{num_dice}d{dice_sides} ({rolls_str})"
    if additional_numbers:
        additional_result = " + " + " + ".join(str(num) for num in additional_numbers)
    else:
        additional_result = ""

    response = f"{ctx.author.mention}\n**Result: {rolls_result}{additional_result}**\n**Total: {total}**\nSeed: {seed}"

    # Delete the command message if the roll is successful
    if rolls:
        await ctx.message.delete()

    await ctx.send(response)

@client.command()
async def help(ctx):
    try:
        with open("help.txt", "r") as file:
            help_text = file.read()
        await ctx.send(help_text)
    except FileNotFoundError:
        await ctx.send("Help text is not available.")

client.run('Your Token Here')