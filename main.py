import os
from flask import Flask, render_template
import weather_backend

# Get the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create Flask app and point it to the templates and static directories
app = Flask(__name__, 
           template_folder=os.path.join(SCRIPT_DIR, 'templates'),
           static_folder=os.path.join(SCRIPT_DIR, 'static'))

@app.route('/')
def home():
    stations = weather_backend.get_stations_info()
    return render_template("home.html", stations=stations)

@app.route('/api/v1/<station>/<date>')
def station_temperature_at_date(station, date):
    try:
        temperature = weather_backend.get_temperature(station, date)
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

@app.route('/api/v1/<station>')
def all_data_for_station(station):
    try:
        data = weather_backend.get_station_data(station)
        return {
            "station": station,
            "data": data.to_dict(orient='records')
        }
    except FileNotFoundError:
        return {"error": "Station not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    
@app.route('/api/v1/yearly/<station>/<year>')
def yearly_data_for_station(station, year):
    try:
        data = weather_backend.get_yearly_data(station, year)
        return {
            "station": station,
            "year": year,
            "data": data.to_dict(orient='records')
        }
    except FileNotFoundError:
        return {"error": "Station not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    

if __name__ == "__main__":
    app.run(debug=True)
