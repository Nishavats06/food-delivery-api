from fastapi import APIRouter, HTTPException, status
from app.core.geocoding import search_location, reverse_geocode

router = APIRouter(prefix="/location", tags=["Location"])


@router.get("/search")
def location_search(q: str):
    results = search_location(q)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No locations found")
    return results


@router.get("/geocode")
def location_geocode(lat: float, lon: float):
    result = reverse_geocode(lat, lon)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return result