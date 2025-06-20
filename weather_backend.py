import os
import pandas as pd
import glob

def get_station_data_file_path(station):
    """
    Construct the file path for a station's data file.
    
    Args:
        station (str or int): The station ID
    
    Returns:
        str: The full file path to the station's data file
    """
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    station_id = str(int(station)).zfill(6)
    return os.path.join(SCRIPT_DIR, 'data_small', f'TG_STAID{station_id}.txt')

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
        filename = get_station_data_file_path(station)
        
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
      # Get the stations file path
    stations_file = os.path.join(SCRIPT_DIR, 'data_small', 'stations.txt')
    
    # Extract station IDs and create a list of stations
    stations = []
    
    try:
        # Read the stations file with pandas
        df = pd.read_csv(stations_file, skiprows=17)
        
        station_name_col = 'STANAME                                 '
        
        # Process each station
        for _, row in df.iterrows():
            station_name = row[station_name_col].strip() if isinstance(row[station_name_col], str) else row[station_name_col].strip()
    
            stations.append({
                'id': str(int(row['STAID'])),
                'location': f"{station_name}"
            })
            
    except FileNotFoundError:
        raise FileNotFoundError("stations.txt file not found")
    except Exception as e:
        raise ValueError(f"Error reading stations file: {str(e)}")

    # Sort stations by ID
    stations.sort(key=lambda x: int(x['id']))
    
    return stations


def get_station_data(station):
    """
    Get all available data for a specific weather station.
    
    Args:
        station (str): The station ID
    
    Returns:
        DataFrame: A pandas DataFrame containing the station's data
    """
    try:
        filename = get_station_data_file_path(station)

        # Read the data file, skipping metadata rows
        df = pd.read_csv(filename, skiprows=20)

        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Station {station} not found")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    


def get_yearly_data(station, year):
    """
    Get all available data for a specific weather station for a specific year.
    
    Args:
        station (str): The station ID
        year (str): The year in YYYY format
    
    Returns:
        DataFrame: A pandas DataFrame containing the station's data for the specified year
    """
    try:
        filename = get_station_data_file_path(station)

        # Read the data file, skipping metadata rows
        df = pd.read_csv(filename, skiprows=20)
        
        # Filter by year
        df['    DATE'] = df['    DATE'].astype(str)
        df = df[df['    DATE'].str.startswith(str(year))]

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Station {station} not found")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")