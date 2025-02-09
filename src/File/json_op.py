
import json 

ZIP_DATA_PATH = "zip_coordinates.json"
DISASTER_HISTORY_PATH = ""
def read_json_file(path):
    """Reads a JSON file and returns its content."""
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return empty dict if file is missing or has invalid JSON


def write_json_file(path, data):
    """Writes data to a JSON file."""
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def search_zip(zipcode, path):
    """Searches for stored coordinates of a given zip code."""
    data = read_json_file(path)
    return data.get(zipcode)





