
from src.File.json_op import read_json_file, write_json_file, search_zip
from datetime import datetime
import os
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CACHED_RESPONSE_PATH = "./Data/Cache/zip_report_cache.json"  # Ensure path is correctly set

def add_new_report(zipcode , new_data):
    """Adds a new report entry for the given zipcode."""
    if not os.path.exists(CACHED_RESPONSE_PATH):
        logging.error("JSON file path is invalid or does not exist.")
        return False
    
    data = read_json_file(CACHED_RESPONSE_PATH)
    data[zipcode] = new_data
    write_json_file(CACHED_RESPONSE_PATH , data)


def if_report_exist(data):
    """Checks if the report exists for the current date."""
    try:
        provided_date = datetime.strptime(data["current_date"], "%Y-%m-%d").date()
        return provided_date == datetime.today().date()
    except (KeyError, ValueError) as e:
        logging.error(f"Invalid date format or missing key: {e}")
        return False


        
def update_report(zipcode):
    """Updates the report if it exists; otherwise, removes outdated entries."""
    if not os.path.exists(CACHED_RESPONSE_PATH):
        logging.error("JSON file path is invalid or does not exist.")
        return None

    response = search_zip(zipcode, CACHED_RESPONSE_PATH)
    
    if response:
        if if_report_exist(response):
            logging.info(f"Report for {zipcode} is up to date.")
            return response
        else:
            data = read_json_file(CACHED_RESPONSE_PATH) 
            if zipcode in data:
                del data[zipcode]  # Remove outdated entry
                write_json_file(CACHED_RESPONSE_PATH, data)
                logging.info(f"Outdated report for {zipcode} removed.")
            return None
    else:
        logging.warning(f"No existing report found for {zipcode}.")
        return None

        
# # Example: provided date in string format (e.g., "2025-02-01")
# provided_date_str = "2025-02-01"

# # Convert the provided date string to a datetime object
# provided_date = datetime.strptime(provided_date_str, "%Y-%m-%d").date()

# # Get today's date
# today_date = datetime.today().date()

# # Check if the dates are equal
# if provided_date == today_date:
#     print("The provided date is today.")
# else:
#     print("The provided date is not today.")
