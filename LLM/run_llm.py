from ollama import chat
from ollama import ChatResponse
import json 

# report format.
data = {
    "current_date":"2025-01-28",
    "weather": {
        "data": {
            "lat": 12.9716,
            "lng": 77.5946,
            "timezone": "Asia/Kolkata",
            "country_code": "IN",
            "time": 1719302400,
            "apparentTemperature": 29.5,
            "cloudCover": 20,
            "dewPoint": 18.5,
            "humidity": 75,
            "pressure": 1012,
            "precipIntensity": 0.35,
            "temperature": 28.5,
            "visibility": 10.0,
            "windGust": 28.0,
            "ozone": 275.0,
            "uvIndex": 5.0,
            "windSpeed": 15.0,
            "windBearing": 270,
            "icon": "rain",
            "summary": "Expect thunderstorms with moderate humidity. Windy conditions.",
            "updatedAt": "2024-06-25T08:00:00.000Z"
        }
    },
    "air_quality": {
        "stations": [
            {
                "CO": 1.0,
                "NO2": 18.5,
                "OZONE": 8.5,
                "PM10": 55.0,
                "PM25": 22.5,
                "SO2": 2.0,
                "city": "Bangalore",
                "countryCode": "IN",
                "division": "Bangalore",
                "lat": 12.9716,
                "lng": 77.5946,
                "placeName": "M.G. Road",
                "postalCode": "560001",
                "state": "Karnataka",
                "updatedAt": "2024-06-25T08:00:00.000Z",
                "AQI": 90,
                "aqiInfo": {
                    "pollutant": "PM2.5",
                    "concentration": 22.5,
                    "category": "Moderate"
                }
            }
        ]
    },
    "today_disaster": {
        "result": [
            {
                "event_type": "Flood",
                "event_name": "South Bangalore Flood",
                "date": "2025-01-28 16:00:00",
                "lat": 12.9538,
                "lng": 77.6000,
                "continent": "Asia",
                "created_time": "2025-01-28 18:00:00",
                "source_event_id": "123456789",
                "event_id": "abc123xyz"
            }
        ]
    },
    "disaster_history": {
        "result": [
            {
                "event_type": "Flood",
                "event_name": "Annual Monsoon Flood in Bangalore",
                "date": "2023-07-15 00:00:00",
                "lat": 12.9538,
                "lng": 77.6000,
                "continent": "Asia",
                "created_time": "2023-07-16 10:00:00",
                "source_event_id": "101234567",
                "event_id": "def456ghi"
            }
        ]
    },
    "contact_information": {
        "emergency_numbers": {
            "Police": "100",
            "Fire Department": "101",
            "Ambulance": "102"
        },
        "websites": {
            "Local Police": "http://bangalorepolice.gov",
            "Red Cross": "http://redcross.org",
            "Club": "http://daneclub.org"
        }
    }
}


def process_report(data):
    try: 
        response: ChatResponse = chat(model='Hermes_Disaster_Managment:latest', messages=[
        {   
            "role":"user",
            "content":f"{data}"
        },])
        
        result = response.message.content 
        
        if result:
            return json.dumps(result)
        else:
            return None 
    except Exception as e:
        print(f"Error processing report: {e}")
        return json.dumps({"error": str(e)}) 

