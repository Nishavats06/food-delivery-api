from fastapi import APIRouter, HTTPException, status
from app.core.geocoding import search_location, reverse_geocode
from app.schemas.location import GeocodeResponse, SearchResponse

router = APIRouter(prefix="/location", tags=["Location"])


@router.get("/search", response_model=SearchResponse)
def location_search(q: str):
    results = search_location(q)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No locations found")
    return SearchResponse(success=True, message="success", data=results)


@router.get("/geocode", response_model=GeocodeResponse)
def location_geocode(lat: float, lon: float):
    result = reverse_geocode(lat, lon)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return GeocodeResponse(success=True, message="success", data=result)