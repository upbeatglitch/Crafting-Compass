from flask import Flask, render_template, request

app = Flask(__name__)

# --- Crystal Data Dictionary ---
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

# --- FIX 1: ADDED MISSING DICTIONARY FOR HQ CONDITION LOOKUP ---
HQ_CONDITION_LOOKUP = {
    data["hq"].lower().replace(' ', ''): crystal_key
    for crystal_key, data in CRYSTAL_DATA.items()
}

# --- Create a reverse lookup for the new HQ names ---
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
    hq_name: crystal_key
    for hq_name, crystal_key in HQ_NAME_MAP.items()
}

@app.route('/', methods=['GET', 'POST'])
def crafting_compass():
    result = None
    crystal_input = None

    if request.method == 'POST':
        crystal_input = request.form.get('crystal_name', '').strip()
        normalized_input = crystal_input.lower().replace(' crystal', '').replace(' ', '')

        crystal_key = None
        data = None

        # 1. Look up by primary crystal key
        if normalized_input in CRYSTAL_DATA:
            crystal_key = normalized_input
        
        # 2. Look up by the HQ Name alias
        elif normalized_input in HQ_NAME_LOOKUP:
            crystal_key = HQ_NAME_LOOKUP.get(normalized_input)
        
        # 3. Look up by the HQ Condition string
        elif normalized_input in HQ_CONDITION_LOOKUP:
            crystal_key = HQ_CONDITION_LOOKUP.get(normalized_input)
            
        if crystal_key:
            data = CRYSTAL_DATA.get(crystal_key)

        # Process the result
        if data:
            result = {
                "name": data["name"],
                "hq": data["hq"],
                "success": data["success"],  # <-- FIX 2: COMMA IS HERE
                "escutcheon enchantment HQ": data["escutcheon enchantment HQ"]
            }
        else:
            example_names = ['Earth', 'Fire', 'Terra', 'Inferno']
            example_condition = CRYSTAL_DATA['earth']['hq']
            result = {
                "name": "Crystal Not Found", 
                "hq": "N/A", 
                "success": f"Please enter a valid crystal name (e.g., '{example_names[0]}', '{example_names[2]}') or the full HQ crafting conditions (e.g., '{example_condition}').",
                "escutcheon enchantment HQ": "N/A"
            }

    return render_template('compass.html', result=result, crystal_input=crystal_input)

# --- Run the Application ---
if __name__ == '__main__':
    app.run(debug=True)