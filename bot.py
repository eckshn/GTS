import re
import json
import os
import discord
from discord.ext import commands
from initial import load_cards, get_card_id

# Read token from file
with open("tokens.txt", "r") as file:
    TOKEN = file.readline().strip()

# Load all card databases from the folder
cards_dict = load_cards()

intents = discord.Intents.default()
intents.message_content = True

intents = discord.Intents.default()
intents.message_content = True

discord = commands.Bot(command_prefix='!', intents=intents)

# Pattern matches "- PokemonName [EX]"
EXPANSIONS = ["GA", "MI", "ST", "TL", "SR", "CG"]
POKE_PATTERN = re.compile(r"-\s*(\w+)\s*((e|E)(x|X))?\s*\((GA|MI|ST|TL|SR|CG)\)")

@discord.event
async def on_ready():
    print(f'Logged in as {discord.user}!')

@discord.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("GTS"):
        # Get the message timestamp
        message_time = message.created_at

        content = message.content
        # Split by sections
        lf_matches = []
        ft_matches = []

        # Normalize line breaks and split into sections
        lines = content.splitlines()
        current_section = None

        for line in lines:
            line = line.strip()
            if line.upper() == "LF":
                current_section = "LF"
            elif line.upper() == "FT":
                current_section = "FT"
            else:
                match = POKE_PATTERN.match(line)
                if not match:
                    continue
                for i, group in enumerate(match.groups()):
                    print(i, group)
                pokemon, expansion = match.group(2), match.group(6)
                print(pokemon, expansion)
                card_id = get_card_id(pokemon, expansion)

                if current_section == "LF":
                    lf_matches.append(card_id)
                elif current_section == "FT":
                    ft_matches.append(card_id)

        # Log results
        print(f"User: {message.author}")
        print(f"LF Matches: {lf_matches}")
        print(f"FT Matches: {ft_matches}")

        # Optional: reply to the user
        if lf_matches or ft_matches:
            await message.channel.send(
                f"{message.author.mention} GTS parsed:\n"
                f"**LF**: {', '.join(lf_matches) if lf_matches else 'None'}\n"
                f"**FT**: {', '.join(ft_matches) if ft_matches else 'None'}"
            )

discord.run(TOKEN)