import os
import glob
from flask import Flask, render_template
from weather_backend import get_temperature

# Get the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create Flask app and point it to the templates directory
app = Flask("__name__", template_folder=os.path.join(SCRIPT_DIR, 'templates'))

@app.route('/')
def home():
    # Get all station files
    station_files = glob.glob(os.path.join(SCRIPT_DIR, 'data_small', 'TG_STAID*.txt'))
    
    # Extract station IDs and create a list of stations
    stations = []
    for file in station_files:
        # Extract station ID from filename (remove 'TG_STAID' prefix and '.txt' suffix)
        station_id = os.path.basename(file)[8:14]  # Get the 6 digits
        
        # Read first few lines to get station info (if available)
        try:
            with open(file, 'r', encoding='utf-8') as f:
                # Skip header lines
                for _ in range(20):  # Skip first 20 lines
                    next(f)
                # Read first data line to get SOUID
                first_line = next(f).strip().split(',')
                station_number = first_line[0].strip()
                stations.append({
                    'id': station_id,
                    'number': station_number
                })
        except (IOError, IndexError, UnicodeDecodeError):
            # If there's any error reading the file, just add the ID
            stations.append({'id': station_id, 'number': station_id})
    
    # Sort stations by ID
    stations.sort(key=lambda x: int(x['id']))
    
    return render_template("home.html", stations=stations)

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
