import os
import glob
from flask import Flask, render_template
from weather_backend import get_temperature

# Get the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create Flask app and point it to the templates and static directories
app = Flask(__name__, 
           template_folder=os.path.join(SCRIPT_DIR, 'templates'),
           static_folder=os.path.join(SCRIPT_DIR, 'static'))

@app.route('/')
def home():
    # Get all station files
    station_files = glob.glob(os.path.join(SCRIPT_DIR, 'data_small', 'TG_STAID*.txt'))
    
    # Extract station IDs and create a list of stations
    stations = []
    for file in station_files:
        # Extract station ID from filename (remove 'TG_STAID' prefix and '.txt' suffix)
        station_id = str(int(os.path.basename(file)[8:14]))  # Get the 6 digits and remove leading zeros
        
        # Read file to get station info
        try:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Get the station information line (line 17)
                station_info_line = lines[16]  # 16 because zero-based index
                
                # Extract city and country
                # Format: "This is the blended series of station FALUN, SWEDEN (STAID: 2)"
                location_info = station_info_line.split('station ')[1].split(' (STAID')[0].strip()
                
                stations.append({
                    'id': station_id,
                    'location': location_info
                })
        except (IOError, IndexError, UnicodeDecodeError):
            # If there's any error reading the file, just add the ID
            stations.append({
                'id': station_id,
                'location': 'Unknown Location'
            })
    
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
