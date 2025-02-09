import requests
import geocoder
from typing import Optional, Tuple

def get_location_geocoder() -> Tuple[Optional[float], Optional[float]]:
    """
    Get location using geocoder library
    """
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng[0], g.latlng[1]
    return None, None



def get_location_ipapi() -> Tuple[Optional[float], Optional[float]]:
    """
    Fallback method using ipapi.co service
    """
    try:
        response = requests.get('https://ipapi.co/json/')
        if response.status_code == 200:
            data = response.json()
            lat = data.get('latitude')
            lon = data.get('longitude')
            
            if lat is not None and lon is not None:
                return lat, lon
    except requests.RequestException as e:
        print(f"Error retrieving location from ipapi.co: {str(e)}")
    return None, None

def get_location() -> Tuple[Optional[float], Optional[float]]:
    """
    Tries to get location first using geocoder, then falls back to ipapi.co
    """
    # Try geocoder first
    lat, lon = get_location_geocoder()
    
    # If geocoder fails, try ipapi
    if lat is None:
        print("Primary geolocation method unsuccessful, trying alternative...")
        lat, lon = get_location_ipapi()
    
    return lat, lon

