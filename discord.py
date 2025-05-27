import re
import discord
from discord.ext import commands

# Read token from file
with open("tokens.txt", "r") as file:
    TOKEN = file.readline().strip()

intents = discord.Intents.default()
intents.message_content = True

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Pattern matches "- PokemonName [EX]"
poke_pattern = re.compile(r"-\s*(\w+)\s*(\[EX\])?")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("GTS"):
        content = message.content
        # Split by sections
        lf_matches = []
        tf_matches = []

        # Normalize line breaks and split into sections
        lines = content.splitlines()
        current_section = None

        for line in lines:
            line = line.strip()
            if line.upper() == "LF":
                current_section = "LF"
            elif line.upper() == "TF":
                current_section = "TF"
            else:
                match = poke_pattern.match(line)
                if match:
                    pokemon = match.group(1)
                    if current_section == "LF":
                        lf_matches.append(pokemon)
                    elif current_section == "TF":
                        tf_matches.append(pokemon)

        # Log results
        print(f"User: {message.author}")
        print(f"LF Matches: {lf_matches}")
        print(f"TF Matches: {tf_matches}")

        # Optional: reply to the user
        if lf_matches or tf_matches:
            await message.channel.send(
                f"{message.author.mention} GTS parsed:\n"
                f"**LF**: {', '.join(lf_matches) if lf_matches else 'None'}\n"
                f"**TF**: {', '.join(tf_matches) if tf_matches else 'None'}"
            )

bot.run(TOKEN)