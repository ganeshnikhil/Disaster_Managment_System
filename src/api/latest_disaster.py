import http.client
from dotenv import load_dotenv
from os import getenv
import json 

load_dotenv()
ambeedata_api = getenv("ambeedata_api")


def latest_disaster_report(coordinates):
    """Fetches the latest disaster data for given coordinates."""
    if not ambeedata_api:
        print("Error: API key is missing.")
        return None
    
    conn = http.client.HTTPSConnection("api.ambeedata.com")
    lng , lat = coordinates
    endpoint = f"/disasters/latest/by-lat-lng?lat={lat}&lng={lng}"
    
    headers = {
        'x-api-key': ambeedata_api,
        'Content-type': "application/json"
    }
    
    try:
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        if res.status != 200:
            print(f"API request failed with status {res.status}")
            return None
        
        data = res.read()
        return json.loads(data.decode("utf-8"))
    
    except Exception as e:
        print(f"Request failed: {e}")
        return None
    
    finally:
        conn.close()
