import os
import pandas as pd

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
