from src.api.air_qualtiy import air_quality_report
from src.api.weather import weather_report
from src.api.latest_disaster import latest_disaster_report
from src.api.historical_data import historical_disaster_report , hist_disaster_report
from src.api.zip_coordinates import get_zip_coordinates 
from Data.Const.constants import INPUT_TEMPLATE
from datetime import datetime


def assemble(zipcode):
    # Get today's date and format it as "YYYY-MM-DD"
    today_date = datetime.today().strftime("%Y-%m-%d")
    
    # Make a copy of the INPUT_TEMPLATE to avoid direct modification
    template = INPUT_TEMPLATE.copy()
    template["current_date"] = today_date

    try:
        # Get coordinates from the zipcode
        coordinates = get_zip_coordinates(zipcode)

        # Fetch weather data
        weather = weather_report(coordinates)
        template["weather"]["data"] = weather.get("data", {})

        # Fetch air quality data
        air = air_quality_report(coordinates)
        template["air_quality"]["stations"] = air.get("stations", [])

        # Fetch latest disaster data
        today_disaster = latest_disaster_report(coordinates)
        result_data = today_disaster.get("result") or today_disaster.get("data")
        template["today_disaster"]["result"] = result_data

        # Fetch historical disaster data
        history_report = historical_disaster_report(zipcode, coordinates)
        template["disaster_history"] = history_report

    except Exception as e:
        # Handle errors and provide an informative message
        template["error"] = f"Error fetching data: {str(e)}"
        return {}

    return template

def assemble_coordinates(coordinates):
    # Get today's date and format it as "YYYY-MM-DD"
    today_date = datetime.today().strftime("%Y-%m-%d")
    
    # Make a copy of the INPUT_TEMPLATE to avoid direct modification
    template = INPUT_TEMPLATE.copy()
    template["current_date"] = today_date

    try:
        # Fetch weather data
        weather = weather_report(coordinates)
        template["weather"]["data"] = weather.get("data", {})

        # Fetch air quality data
        air = air_quality_report(coordinates)
        template["air_quality"]["stations"] = air.get("stations", [])

        # Fetch latest disaster data
        today_disaster = latest_disaster_report(coordinates)
        result_data = today_disaster.get("result") or today_disaster.get("data")
        template["today_disaster"]["result"] = result_data
        
        # Fetch historical disaster data
        history_report = hist_disaster_report(coordinates)
        template["disaster_history"] = history_report

    except Exception as e:
        # Handle errors and provide an informative message
        template["error"] = f"Error fetching data: {str(e)}"
        return {}

    return template
