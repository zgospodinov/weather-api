import os
import pandas as pd
import glob

def get_temperature(station, date):
    """
    Get the temperature for a specific station on a specific date.
    
    Args:
        station (str): The station ID
        date (str): The date in YYYYMMDD format
    
    Returns:
        float: The temperature in degrees Celsius
        
    Raises:
        FileNotFoundError: If the station file doesn't exist
        IndexError: If the date is not found in the data
        ValueError: If the input parameters are invalid
    """
    try:
        # Get the directory containing this script
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Convert station to proper file format (e.g., 1 -> "000001")
        station_id = str(int(station)).zfill(6)
        filename = os.path.join(SCRIPT_DIR, 'data_small', f'TG_STAID{station_id}.txt')
        
        # Read the data file, skipping metadata rows
        df = pd.read_csv(filename, skiprows=20)
        
        # Filter by date and get temperature
        temperature = df[df['    DATE'] == int(date)]['   TG'].iloc[0]
        
        # Convert temperature from tenths of degrees to actual degrees
        return temperature / 10
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Station {station} not found")
    except IndexError:
        raise IndexError(f"No data found for station {station} on date {date}")
    except ValueError as e:
        raise ValueError(f"Invalid input parameters: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

def get_stations_info():
    """
    Get information about all available weather stations.
    
    Returns:
        list: A list of dictionaries containing station information:
              - id: station ID (string)
              - location: city and country (string)
    """
    # Get the directory containing this script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
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
    
    return stations
