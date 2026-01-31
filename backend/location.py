"""
Location Detection Service
Gets geographic location from IP address
Uses ipapi.co free API (no authentication required)
"""

import requests
from typing import Dict


def get_location_from_ip(ip_address: str = None) -> Dict:
    """
    Get location details from IP address
    
    Args:
        ip_address: Optional IP address. If None, uses requester's IP
    
    Returns:
        dict: {
            'ip': str,
            'city': str,
            'region': str,
            'country': str,
            'latitude': float,
            'longitude': float,
            'timezone': str
        }
    """
    
    try:
        # Use ipapi.co free service
        if ip_address:
            url = f"https://ipapi.co/{ip_address}/json/"
        else:
            url = "https://ipapi.co/json/"
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            return {
                "ip": data.get("ip", "Unknown"),
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "latitude": data.get("latitude", 0.0),
                "longitude": data.get("longitude", 0.0),
                "timezone": data.get("timezone", "Unknown"),
                "postal": data.get("postal", "Unknown")
            }
        
        else:
            print(f"⚠️ Location API returned status {response.status_code}")
            return get_fallback_location()
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Location API request failed: {str(e)}")
        return get_fallback_location()
    
    except Exception as e:
        print(f"⚠️ Error getting location: {str(e)}")
        return get_fallback_location()


def get_fallback_location() -> Dict:
    """
    Fallback location when API fails
    Returns default location (Delhi, India)
    """
    
    return {
        "ip": "Unknown",
        "city": "New Delhi",
        "region": "Delhi",
        "country": "India",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata",
        "postal": "110001"
    }


def reverse_geocode(latitude: float, longitude: float) -> Dict:
    """
    Convert coordinates to address (reverse geocoding)
    Uses OpenStreetMap Nominatim API (free, no auth required)
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    
    Returns:
        dict: Address information
    """
    
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json"
        }
        headers = {
            "User-Agent": "AccidentDetectionSystem/1.0"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            
            return {
                "address": data.get("display_name", "Unknown"),
                "city": address.get("city") or address.get("town") or address.get("village", "Unknown"),
                "state": address.get("state", "Unknown"),
                "country": address.get("country", "Unknown"),
                "postcode": address.get("postcode", "Unknown")
            }
        
        else:
            return {"address": "Unknown", "city": "Unknown"}
    
    except Exception as e:
        print(f"⚠️ Reverse geocoding failed: {str(e)}")
        return {"address": "Unknown", "city": "Unknown"}


def format_location_string(location_data: Dict) -> str:
    """
    Format location data into readable string
    
    Args:
        location_data: Location dictionary
    
    Returns:
        Formatted location string
    """
    
    city = location_data.get("city", "Unknown")
    region = location_data.get("region", "")
    country = location_data.get("country", "Unknown")
    
    if region and region != city:
        return f"{city}, {region}, {country}"
    else:
        return f"{city}, {country}"


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
    
    Returns:
        Distance in kilometers
    """
    
    from math import radians, sin, cos, sqrt, atan2
    
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    
    return round(distance, 2)


def get_nearby_hospitals(latitude: float, longitude: float, radius_km: float = 5) -> list:
    """
    Find nearby hospitals using Overpass API (OpenStreetMap)
    
    Args:
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Search radius in kilometers
    
    Returns:
        List of nearby hospitals
    """
    
    try:
        # Convert km to meters for API
        radius_m = radius_km * 1000
        
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        (
          node["amenity"="hospital"](around:{radius_m},{latitude},{longitude});
          way["amenity"="hospital"](around:{radius_m},{latitude},{longitude});
          relation["amenity"="hospital"](around:{radius_m},{latitude},{longitude});
        );
        out center;
        """
        
        response = requests.get(overpass_url, params={"data": overpass_query}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            hospitals = []
            
            for element in data.get("elements", []):
                name = element.get("tags", {}).get("name", "Unnamed Hospital")
                
                # Get coordinates
                if element["type"] == "node":
                    hlat = element.get("lat")
                    hlon = element.get("lon")
                else:
                    hlat = element.get("center", {}).get("lat")
                    hlon = element.get("center", {}).get("lon")
                
                if hlat and hlon:
                    distance = calculate_distance(latitude, longitude, hlat, hlon)
                    hospitals.append({
                        "name": name,
                        "latitude": hlat,
                        "longitude": hlon,
                        "distance_km": distance
                    })
            
            # Sort by distance
            hospitals.sort(key=lambda x: x["distance_km"])
            
            return hospitals[:5]  # Return top 5 nearest
        
        else:
            print(f"⚠️ Overpass API returned status {response.status_code}")
            return []
    
    except Exception as e:
        print(f"⚠️ Error fetching hospitals: {str(e)}")
        return []


# Testing
if __name__ == "__main__":
    print("Testing Location Service...\n")
    
    # Get current location
    print("1. Getting location from IP:")
    location = get_location_from_ip()
    print(f"   Location: {format_location_string(location)}")
    print(f"   Coordinates: {location['latitude']}, {location['longitude']}")
    
    # Reverse geocoding
    print("\n2. Reverse geocoding test:")
    address = reverse_geocode(28.6139, 77.2090)
    print(f"   Address: {address['address']}")
    
    # Distance calculation
    print("\n3. Distance calculation:")
    dist = calculate_distance(28.6139, 77.2090, 28.5355, 77.3910)
    print(f"   Distance: {dist} km")
    
    # Nearby hospitals
    print("\n4. Finding nearby hospitals:")
    hospitals = get_nearby_hospitals(28.6139, 77.2090)
    print(f"   Found {len(hospitals)} hospitals")
    for h in hospitals[:3]:
        print(f"   - {h['name']}: {h['distance_km']} km away")