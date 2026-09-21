from fastapi import APIRouter, HTTPException, status, Query, Depends
from app.core.geocoding import search_location, reverse_geocode
from app.schemas.location import GeocodeResponse, SearchResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/location", tags=["Location"])


@router.get("/search", response_model=SearchResponse)
def location_search(
    query: str = Query(..., description="Free-text address or place name", example="221B Baker Street, Bengaluru"),
    lat: str = Query(None, description="Latitude bias — pair with lng to bias results nearby (within 200km)", example="12.9716"),
    lng: str = Query(None, description="Longitude bias — pair with lat to bias results nearby (within 200km)", example="77.5946"),
    current_user: User = Depends(get_current_user),
):
    lat_f = None
    lng_f = None
    if lat is not None and lng is not None:
        try:
            lat_f = float(lat)
            lng_f = float(lng)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="lat and lng must be valid numbers")

    results = search_location(query, lat=lat_f, lng=lng_f)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No locations found")
    return SearchResponse(success=True, message="success", data=results)


@router.get("/geocode", response_model=GeocodeResponse)
def location_geocode(
    lat: str = Query(..., description="Latitude as a number-string", example="12.9716"),
    lng: str = Query(..., description="Longitude as a number-string", example="77.5946"),
    current_user: User = Depends(get_current_user),
):
    try:
        lat_f = float(lat)
        lng_f = float(lng)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="lat and lng must be valid numbers")

    result = reverse_geocode(lat_f, lng_f)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return GeocodeResponse(success=True, message="success", data=result)