import httpx

NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"
HEADERS = {"User-Agent": "food-delivery-app"}


def search_location(query: str, limit: int = 5) -> list[dict]:
    try:
        response = httpx.get(
            NOMINATIM_SEARCH_URL,
            params={"q": query, "format": "json", "limit": limit},
            headers=HEADERS,
            timeout=5.0,
        )
        response.raise_for_status()
        results = response.json()
        return [
            {
                "display_name": r["display_name"],
                "latitude": float(r["lat"]),
                "longitude": float(r["lon"]),
            }
            for r in results
        ]
    except Exception:
        return []


def reverse_geocode(lat: float, lon: float) -> dict | None:
    try:
        response = httpx.get(
            NOMINATIM_REVERSE_URL,
            params={"lat": lat, "lon": lon, "format": "json", "addressdetails": 1},
            headers=HEADERS,
            timeout=5.0,
        )
        response.raise_for_status()
        result = response.json()
        if "display_name" not in result:
            return None

        address = result.get("address", {})
        road = address.get("road")
        house_number = address.get("house_number")
        address_line1 = f"{house_number} {road}".strip() if house_number or road else None

        return {
            "formattedAddress": result["display_name"],
            "addressLine1": address_line1,
            "addressLine2": address.get("suburb") or address.get("neighbourhood"),
            "city": address.get("city") or address.get("town") or address.get("village"),
            "state": address.get("state"),
            "country": address.get("country"),
            "pincode": address.get("postcode"),
            "latitude": lat,
            "longitude": lon,
        }
    except Exception:
        return None