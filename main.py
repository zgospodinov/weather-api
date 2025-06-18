import os
from flask import Flask, render_template

# Get the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create Flask app and point it to the templates directory
app = Flask("__name__", template_folder=os.path.join(SCRIPT_DIR, 'templates'))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api/v1/<station>/<date>')
def station_temperature_at_date(station, date):
    temperature = 25
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }

if( __name__ == "__main__"):
    app.run(debug=True)
