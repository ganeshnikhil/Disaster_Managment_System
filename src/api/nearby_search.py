from requests.structures import CaseInsensitiveDict
import requests 
import json 
from dotenv import load_dotenv
from os import getenv

load_dotenv()
geoapify_key = getenv("geoapify_key")

# 3 thousand credit per day , request in sec < 5 , 
# every 20 places costing 1 credit
# limit the parameter.

  
def format_it(data):
    nearby_info = []
    list_of_features = data.get("features",None)
    
    if list_of_features:
        for details in list_of_features:
            temp = {}
            temp["name"] = details.get("properties", {}).get("name")
            temp["lon"] = details.get("properties", {}).get("lon")
            temp["lat"] = details.get("properties", {}).get("lat")
            temp["dist"] = details.get("properties", {}).get("distance")
            list_of_cat = details.get("properties", {}).get("categories", [])
            temp["address"] = details.get("properties", {}).get("address_line2")
            if list_of_cat:
                if "healthcare.pharmacy" in list_of_cat:
                    temp["type"] = "pharmacy"
                if "healthcare.hospital" in list_of_cat:
                    temp["type"] = "hospital"
            nearby_info.append(temp)
    return nearby_info


def get_nearby_healthcare(lat, lng,limit=3):
    """
    Fetches nearby hospitals and pharmacies using the Geoapify API.
    """
    url = f"https://api.geoapify.com/v2/places?categories=healthcare.hospital,healthcare.pharmacy&bias=proximity:{lng},{lat}&limit={limit}&apiKey={geoapify_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        all_adresses = response.json()
        return format_it(all_adresses)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
    
if __name__ == "__main__":
    lat = 28.5915
    lng = 77.0531
    data = get_nearby_healthcare(lat , lng)
    print(json.dumps(data,indent=4))
    
    
'''
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Rai Medico",
                "country": "India",
                "country_code": "in",
                "state": "Delhi",
                "county": "Dwarka Tehsil",
                "state_district": "South West Delhi",
                "city": "Dwarka",
                "postcode": "110075",
                "district": "Sector 10",
                "street": "Road 221",
                "lon": 77.0563222,
                "lat": 28.5892292,
                "state_code": "DL",
                "formatted": "Rai Medico, Road 221, Sector 10, Dwarka - 110075, Delhi, India",
                "address_line1": "Rai Medico",
                "address_line2": "Road 221, Sector 10, Dwarka - 110075, Delhi, India",
                "categories": [
                    "commercial.health_and_beauty",
                    "commercial.health_and_beauty.pharmacy",
                    "healthcare.pharmacy"
                ],
                "details": [],
                "datasource": {
                    "sourcename": "openstreetmap",
                    "attribution": "\u00a9 OpenStreetMap contributors",
                    "license": "Open Database License",
                    "url": "https://www.openstreetmap.org/copyright",
                    "raw": {
                        "name": "Rai Medico",
                        "osm_id": 993723048,
                        "amenity": "pharmacy",
                        "osm_type": "n"
                    }
                },
                "distance": 403,
                "place_id": "517bc26dc89a4353405996568fb9d7963c40f00103f901a8023b3b0000000092030a526169204d656469636f"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    77.0563222,
                    28.589229199881252
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": 98.3,
                "country": "India",
                "country_code": "in",
                "state": "Delhi",
                "county": "Dwarka Tehsil",
                "state_district": "South West Delhi",
                "city": "Dwarka",
                "postcode": "110075",
                "district": "Sector 10",
                "street": "Central Road",
                "lon": 77.0589614,
                "lat": 28.5902843,
                "state_code": "DL",
                "formatted": "98.3, Central Road, Sector 10, Dwarka - 110075, Delhi, India",
                "address_line1": "98.3",
                "address_line2": "Central Road, Sector 10, Dwarka - 110075, Delhi, India",
                "categories": [
                    "commercial.health_and_beauty",
                    "commercial.health_and_beauty.pharmacy",
                    "healthcare.pharmacy"
                ],
                "details": [],
                "datasource": {
                    "sourcename": "openstreetmap",
                    "attribution": "\u00a9 OpenStreetMap contributors",
                    "license": "Open Database License",
                    "url": "https://www.openstreetmap.org/copyright",
                    "raw": {
                        "name": 98.3,
                        "osm_id": 993723109,
                        "amenity": "pharmacy",
                        "osm_type": "n"
                    }
                },
                "distance": 589,
                "place_id": "517d2e0906c643534059ed5433df1c973c40f00103f901e5023b3b0000000092030439382e33"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    77.0589614,
                    28.590284299881137
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Ayushman Hospital",
                "country": "India",
                "country_code": "in",
                "state": "Delhi",
                "county": "Dwarka Tehsil",
                "state_district": "South West Delhi",
                "city": "Dwarka",
                "postcode": "110075",
                "district": "Sector 12",
                "street": "Desh Bandhu Gupta Marg",
                "lon": 77.0493833,
                "lat": 28.5965201,
                "state_code": "DL",
                "formatted": "Ayushman Hospital, Desh Bandhu Gupta Marg, Sector 12, Dwarka - 110075, Delhi, India",
                "address_line1": "Ayushman Hospital",
                "address_line2": "Desh Bandhu Gupta Marg, Sector 12, Dwarka - 110075, Delhi, India",
                "categories": [
                    "healthcare.hospital"
                ],
                "details": [
                    "details",
                    "details.contact"
                ],
                "datasource": {
                    "sourcename": "openstreetmap",
                    "attribution": "\u00a9 OpenStreetMap contributors",
                    "license": "Open Database License",
                    "url": "https://www.openstreetmap.org/copyright",
                    "raw": {
                        "name": "Ayushman Hospital",
                        "osm_id": 992920693,
                        "amenity": "hospital",
                        "osm_type": "n",
                        "addr:full": "Plot No. 2, Dwarka, Sector 12",
                        "addr:state": "Delhi",
                        "description": "<100 Bedded Hospital",
                        "addr:district": "South West",
                        "addr:postcode": 110075,
                        "contact:phone": 42811114
                    }
                },
                "description": "<100 Bedded Hospital",
                "contact": {
                    "phone": 42811114
                },
                "distance": 665,
                "place_id": "51fd9d92182943534059a964908ab5983c40f00103f90175c42e3b0000000092031141797573686d616e20486f73706974616c"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    77.0493833,
                    28.596520099880454
                ]
            }
        }
    ]
}

'''