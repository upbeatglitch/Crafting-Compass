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

# --- Route for the Home Page and Logic ---
@app.route('/', methods=['GET', 'POST'])
def crafting_compass():
    # Initial message before any search
    result = None
    crystal_input = None
    
    # Check if the user has submitted the form
    if request.method == 'POST':
        # Get the input from the web form and convert to lowercase
        crystal_input = request.form.get('crystal_name', '').lower().replace(' crystal', '')
        
        # Look up the data in the dictionary
        data = CRYSTAL_DATA.get(crystal_input)
        
        if data:
            # Crystal found, package the result data
            result = {
                "name": data["name"],
                "hq": data["hq"],
                "success": data["success"],
                "escutcheon enchantment HQ": data["escutcheon enchantment HQ"]
            }
        else:
            # Crystal not found
            result = {"name": "Crystal Not Found", "hq": "N/A", "success": "Please enter a valid crystal name (e.g., 'earth', 'wind')."}

    # Render the HTML template, passing the result data to display
    return render_template('compass.html', result=result, crystal_input=crystal_input)

# --- Run the Application ---
if __name__ == '__main__':
    # Set debug=True for easier development/testing
    app.run(debug=True)