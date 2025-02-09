import requests
from requests.structures import CaseInsensitiveDict
import json
from dotenv import load_dotenv
from os import environ
from src.File.json_op import read_json_file , write_json_file , search_zip
# Load environment variables
load_dotenv()
geoapify_key = environ.get("geoapify_key")

ZIP_DATA_PATH = "./data/Cache/zip_coordinates.json"  # Default file for storing zip-to-coordinates mapping


def add_zip_coord(zipcode, coordinates):
    """Adds a new zip code to coordinates mapping and saves it."""
    data = read_json_file(ZIP_DATA_PATH)
    data[zipcode] = coordinates
    write_json_file(ZIP_DATA_PATH, data)


def zip_to_coordinates(zipcode):
    """Fetches coordinates for a zip code using the Geoapify API."""
    if not geoapify_key:
        print("Error: Geoapify API key is missing.")
        return None
    #"/disasters/history/by-lat-lng?lat=40.4549&lng=36.3025&from=2024-05-31 12:00:00&to=2024-07-31 08:00:00&limit=1&page=1",
    url = (f"https://api.geoapify.com/v1/geocode/search?text={zipcode}&lang=en&limit=10"
           f"&type=postcode&filter=countrycode:in&apiKey={geoapify_key}")
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()  # Raise an exception for HTTP errors
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def get_zip_coordinates(zipcode):
    """Checks local storage for zip coordinates; if not found, fetches from API."""
    coordinates = search_zip(zipcode , ZIP_DATA_PATH)
    if coordinates:
        return coordinates
    
    response = zip_to_coordinates(zipcode)
    print(response)
    #560002
    if response:
        print(response)
        coordinates = response["features"][0]["geometry"]["coordinates"]
        print(coordinates)
        add_zip_coord(zipcode, coordinates)
        return coordinates
    
    print("[+] Coordinates not found for the given zip code.")
    return None
