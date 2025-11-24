from flask import Flask, render_template, request

app = Flask(__name__)

# --- Crystal Data Dictionary ---
# This dictionary holds all your crystal information, making it easy to look up.
CRYSTAL_DATA = {
    "earth": {
        "name": "Earth Crystal",
        "hq": "Darksday, Windsday, New moon, South East",
        "success": "Lightsday, Lightningsday, Full phase, South"
    },
    "wind": {
        "name": "Wind Crystal",
        "hq": "Darksday, Iceday, New moon, East",
        "success": "Lightsday, Earthsday, Full phase, South East"
    },
    "ice": {
        "name": "Ice Crystal",
        "hq": "Darksday, Firesday, New moon, North West",
        "success": "Lightsday, Windsday, Full phase, North"
    },
    "lightning": {
        "name": "Lightning Crystal",
        "hq": "Darksday, Earthsday, New moon, South",
        "success": "Lightsday, Watersday, Full phase, South West"
    },
    "fire": {
        "name": "Fire Crystal",
        "hq": "Darksday, Waterday, New moon, West",
        "success": "Lightsday, Iceday, Full phase, North West"
    },
    "dark": {
        "name": "Dark Crystal",
        "hq": "Darksday, New moon, North East",
        "success": "Lightsday, Full phase, North"
    },
    "light": {
        "name": "Light Crystal",
        "hq": "Lightsday, New moon, North",
        "success": "Lightsday, Full phase, North east"
    },
    "water": {
        "name": "Water Crystal",
        "hq": "Darksday, Lightningsday, New moon, South West",
        "success": "Lightsday, Firesday, Full phase, West"
    }
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
                "success": data["success"]
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