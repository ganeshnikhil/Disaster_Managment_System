'''
100 API calls/day  
info
99 API calls are left for the day 
Can be used for all APIs
Plan Interval: 27 Jan, 2025 - 11 Feb, 2025
'''

import http.client
from urllib.parse import urlparse, quote
from dotenv import load_dotenv
from os import getenv
import json 
from src.File.json_op import read_json_file , write_json_file , search_zip
from datetime import datetime, timezone

load_dotenv()
ambeedata_api = getenv("ambeedata_api")
DISASTER_HISTORY_PATH = "./data/Cache/zip_historical.json"



def to_iso_utc(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    dt_utc = dt.replace(tzinfo=timezone.utc) # Make sure time is treated as UTC
    return dt_utc.isoformat().replace("+00:00", "Z") #

    
def add_zip_history(zipcode,history):
    data = read_json_file(DISASTER_HISTORY_PATH)
    data[zipcode] = history
    write_json_file(DISASTER_HISTORY_PATH , data)
    
    
def historical_disaster_report(zipcode , coordinates):
    history = search_zip(zipcode, DISASTER_HISTORY_PATH)
    
    
    if history:
        return history
    
    from_date_str = "2025-1-25 12:00:00"
    to_date_str = "2025-02-02 08:00:00"
    
    conn = http.client.HTTPSConnection("api.ambeedata.com")
    lng , lat = coordinates
    
    from_iso = to_iso_utc(from_date_str)
    to_iso = to_iso_utc(to_date_str)

    
    headers = {
        'x-api-key': ambeedata_api,
        'Content-type': "application/json"
    }
    lat , lng = coordinates
    url = f"/disasters/history/by-lat-lng?lat={lat}&lng={lng}&from={from_iso}&to={to_iso}&limit=1&page=1".strip()
    conn.request("GET",url, headers=headers)

    res = conn.getresponse()
    
    if res.status != 200:
        print(f"API request failed with status {res.status}.")
        return None
    
    data = res.read()
    response = json.loads(data.decode("utf-8"))
    result_data = response.get("result") or response.get("data")
    history = {"result": result_data}
    add_zip_history(zipcode, history) # Cache the result
    return history


def hist_disaster_report(coordinates):
    
    from_date_str = "2025-1-25 12:00:00"
    to_date_str = "2025-02-02 08:00:00"
    
    conn = http.client.HTTPSConnection("api.ambeedata.com")
    lng , lat = coordinates
    
    from_iso = to_iso_utc(from_date_str)
    to_iso = to_iso_utc(to_date_str)

    
    headers = {
        'x-api-key': ambeedata_api,
        'Content-type': "application/json"
    }
    lat , lng = coordinates
    url = f"/disasters/history/by-lat-lng?lat={lat}&lng={lng}&from={from_iso}&to={to_iso}&limit=1&page=1".strip()
    conn.request("GET",url, headers=headers)

    res = conn.getresponse()
    
    if res.status != 200:
        print(f"API request failed with status {res.status}.")
        return None
    
    data = res.read()
    response = json.loads(data.decode("utf-8"))
    result_data = response.get("result") or response.get("data")
    history = {"result": result_data}
    return history



# def historical_disaster_report(zipcode, coordinates, start_date="2024-12-25 12:00:00", end_date="2025-01-02 08:00:00", limit=1, page=1):
#     """Fetches historical disaster data based on coordinates and date range."""
    
#     history = search_zip(zipcode, DISASTER_HISTORY_PATH)
    
#     # If data is already available, return it
#     if history:
#         return history
    
#     if not ambeedata_api:
#         print("Error: API key is missing.")
#         return None
    
#     from_iso = to_iso_utc(start_date)
#     to_iso = to_iso_utc(end_date)
    
#     lng, lat = coordinates
#     #url = "https://api.ambeedata.com/disasters/history/by-lat-lng"
    
#     headers = {
#         'x-api-key': ambeedata_api,
#         'Content-type': "application/json"
#     } 
#     conn = http.client.HTTPSConnection("api.ambeedata.com")
#     try:
#         url = f"/disasters/history/by-lat-lng?lat={lat}&lng={lng}&from={from_iso}&to={to_iso}&limit=1&page=1".strip()
#         conn.request("GET",url, headers=headers)

#         res = conn.getresponse()
        
#         # Check if the status code indicates a failure
#         if res.status != 200:
#             print(f"API request failed with status {res.status}.")
#             return None
        
#         data = res.read()
#         response = json.loads(data.decode("utf-8"))
        
#         # Check if 'data' is present in the response
#         if "data" not in response:
#             print("No disaster data found for the given date range.")
#             return None
        
#         history = {"result": response["data"]}
        
#         # Add the history data to cache
#         add_zip_history(zipcode, history)
        
#         return history
    
#     except http.client.HTTPException as e:
#         print(f"HTTP error occurred: {e}")
#         return None
    
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON response: {e}")
#         return None
    
#     except Exception as e:
#         print(f"Request failed due to an unexpected error: {e}")
#         return None
    
#     finally:
#         conn.close()  # Ensure the connection is closed even in case of an error