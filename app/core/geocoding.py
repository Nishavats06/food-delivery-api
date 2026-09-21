import httpx
from app.core.config import settings

GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def search_location(query: str, limit: int = 5, lat: float = None, lng: float = None) -> list[dict]:
    try:
        params = {"address": query, "key": settings.GOOGLE_MAPS_API_KEY}
        if lat is not None and lng is not None:
            params["location"] = f"{lat},{lng}"
            params["radius"] = 200000  # 200km in meters

        response = httpx.get(GOOGLE_GEOCODE_URL, params=params, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])[:limit]
        return [
            {
                "formattedAddress": r["formatted_address"],
                "latitude": r["geometry"]["location"]["lat"],
                "longitude": r["geometry"]["location"]["lng"],
            }
            for r in results
        ]
    except Exception:
        return []


def reverse_geocode(lat: float, lon: float) -> dict | None:
    try:
        response = httpx.get(
            GOOGLE_GEOCODE_URL,
            params={"latlng": f"{lat},{lon}", "key": settings.GOOGLE_MAPS_API_KEY},
            timeout=5.0,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return None

        result = results[0]
        components = {c["types"][0]: c["long_name"] for c in result["address_components"] if c["types"]}

        return {
            "formattedAddress": result["formatted_address"],
            "addressLine1": components.get("route"),
            "addressLine2": components.get("sublocality") or components.get("neighborhood"),
            "city": components.get("locality"),
            "state": components.get("administrative_area_level_1"),
            "country": components.get("country"),
            "pincode": components.get("postal_code"),
            "latitude": lat,
            "longitude": lon,
        }
    except Exception:
        return None