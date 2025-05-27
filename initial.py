import json
import os

expansions = {"GA":"Genetic Apex (A1)", "MI":"Mythical Island (A1a)", "ST":"Space-Time Smackdown (A2)", "TL":"Triumphant Light (A2a)", "SR":"Shining Revelry (A2b)", "CG":"Celestial Guardians (A3)"}

def load_cards():
    """Load all card databases from the folder and return a dictionary."""
    cards_dict = {}
    cards_folder = "pokemon-tcg-pocket-card-database/cards/en/"
    
    for filename in os.listdir(cards_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(cards_folder, filename)
            with open(file_path, "r") as file:
                cards_data = json.load(file)
                # Add cards from this file to the main dictionary
                for card in cards_data:
                    cards_dict[card["id"]] = card
    
    return cards_dict

# Need to fix later
def get_card_id(pokemon_name, expansion):
    """Get the card ID for a given Pokemon name and expansion."""
    print(expansion, expansions.keys())
    expansion = expansions[expansion]
    cards_dict = load_cards()
    for card_id, card in cards_dict.items():
        if card["name"] == pokemon_name and card["set"] == expansion:
            return card_id
    return None