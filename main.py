import os
from flask import Flask, render_template
from weather_backend import get_temperature, get_stations_info

# Get the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create Flask app and point it to the templates and static directories
app = Flask(__name__, 
           template_folder=os.path.join(SCRIPT_DIR, 'templates'),
           static_folder=os.path.join(SCRIPT_DIR, 'static'))

@app.route('/')
def home():
    return render_template("home.html", stations=[])

@app.route('/api/v1/<station>/<date>')
def station_temperature_at_date(station, date):
    try:
        temperature = get_temperature(station, date)
        return {
            "station": station,
            "date": date,
            "temperature": temperature
        }
    except FileNotFoundError:
        return {"error": "Station not found"}, 404
    except IndexError:
        return {"error": "Data not found for this date"}, 404
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
