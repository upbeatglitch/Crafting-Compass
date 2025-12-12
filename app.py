from flask import Flask, render_template, request

app = Flask(__name__)

# --- Crystal Data Dictionary ---
# This dictionary holds all your crystal information, making it easy to look up.
CRYSTAL_DATA = {
    "earth": {
        "name": "Earth Crystal",
        "hq": "Darksday, Windsday, New moon, South East",
        "success": "Lightsday, Lightningsday, Full moon, South",
        "escutcheon enchantment HQ": "Earthsday, Lightningsday, New moon, South"
    },
    "wind": {
        "name": "Wind Crystal",
        "hq": "Darksday, Iceday, New moon, East",
        "success": "Lightsday, Earthsday, Full moon, South East",
        "escutcheon enchantment HQ": "Windsday, Earthday, New moon, South East"
    },
    "ice": {
        "name": "Ice Crystal",
        "hq": "Darksday, Firesday, New moon, North West",
        "success": "Lightsday, Windsday, Full moon, North",
        "escutcheon enchantment HQ": "Iceday, Windsday, New moon, North"
    },
    "lightning": {
        "name": "Lightning Crystal",
        "hq": "Darksday, Earthsday, New moon, South",
        "success": "Lightsday, Watersday, Full moon, South West",
        "escutcheon enchantment HQ": "Lightningsday, Watersday, New moon, South West"
    },
    "fire": {
        "name": "Fire Crystal",
        "hq": "Darksday, Waterday, New moon, West",
        "success": "Lightsday, Iceday, Full moon, North West",
        "escutcheon enchantment HQ": "Firesday, Iceday, New moon, North West"
    },
    "dark": {
        "name": "Dark Crystal",
        "hq": "Darksday, New moon, North East",
        "success": "Darksday, Full moon, North",
        "escutcheon enchantment HQ": "Darksday, New Moon, North" 
    },
    "light": {
        "name": "Light Crystal",
        "hq": "Lightsday, New moon, North",
        "success": "Lightsday, Full moon, North East",
        "escutcheon enchantment HQ": "Lightsday, New moon, North East"
    },
    "water": {
        "name": "Water Crystal",
        "hq": "Darksday, Lightningsday, New moon, South West",
        "success": "Lightsday, Firesday, Full moon, West",
        "escutcheon enchantment HQ": "Watersday, Firesday, New moon, West"
    }
}

# --- Create a reverse lookup for the new HQ names (newly added feature) ---
# Maps normalized HQ name alias to the crystal key (e.g., 'fire').
HQ_NAME_MAP = {
    "inferno": "fire",
    "terra": "earth",
    "torrent": "water",
    "cyclone": "wind",
    "glacier": "ice",
    "plasma": "lightning",
    "aurora": "light",
    "twilight": "dark"
}
HQ_NAME_LOOKUP = {
    # Normalize keys by removing spaces
    hq_name: crystal_key
    for hq_name, crystal_key in HQ_NAME_MAP.items()
}

@app.route('/', methods=['GET', 'POST'])
def crafting_compass():
    # Initial message before any search
    result = None
    crystal_input = None

    # Check if the user has submitted the form
    if request.method == 'POST':
        # Get the input from the web form and normalize it for case-insensitive and space-insensitive matching
        crystal_input = request.form.get('crystal_name', '').strip()
        # Remove ' crystal', convert to lowercase, and remove all spaces for aggressive matching
        normalized_input = crystal_input.lower().replace(' crystal', '').replace(' ', '')

        crystal_key = None
        data = None

        # 1. Try to look up by primary crystal key (e.g., 'earth')
        if normalized_input in CRYSTAL_DATA:
            crystal_key = normalized_input
        
        # 2. Try to look up by the HQ Name alias (e.g., 'terra' or 'inferno')
        elif normalized_input in HQ_NAME_LOOKUP:
            crystal_key = HQ_NAME_LOOKUP.get(normalized_input)
        
        # 3. Try the HQ Condition reverse lookup (e.g., 'darksdaywindsdaynewmoon...')
        elif normalized_input in HQ_CONDITION_LOOKUP:
            crystal_key = HQ_CONDITION_LOOKUP.get(normalized_input)
            
        # Get the data if a key was found
        if crystal_key:
            data = CRYSTAL_DATA.get(crystal_key)

        # Process the result
        if data:
            # Crystal found, package the result data.
            result = {
                "name": data["name"],
                "hq": data["hq"],
                "success": data["success"],
                "escutcheon enchantment HQ": data["escutcheon enchantment HQ"]
            }
        else:
            # Crystal not found
            example_names = ['Earth', 'Fire', 'Terra', 'Inferno']
            example_condition = CRYSTAL_DATA['earth']['hq']
            result = {
                "name": "Crystal Not Found", 
                "hq": "N/A", 
                "success": f"Please enter a valid crystal name (e.g., '{example_names[0]}', '{example_names[2]}') or the full HQ crafting conditions (e.g., '{example_condition}').",
                "escutcheon enchantment HQ": "N/A"
            }

    # Render the HTML template, passing the result data to display
    return render_template('compass.html', result=result, crystal_input=crystal_input)

# --- Run the Application ---
if __name__ == '__main__':
    # Set debug=True for easier development/testing
    app.run(debug=True)