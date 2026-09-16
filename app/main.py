from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.openapi.utils import get_openapi

from app.api.auth import router as auth_router
from app.api.restaurants import router as restaurants_router
from app.api.location import router as location_router
from app.api.menu_items import router as menu_router
from app.api.cart import router as cart_router
from app.api.addresses import router as addresses_router
from app.api.orders import router as orders_router
from app.api.reviews import router as reviews_router

app = FastAPI(title="Food Delivery API")
app.include_router(auth_router)
app.include_router(restaurants_router)
app.include_router(location_router)
app.include_router(menu_router)
app.include_router(cart_router)
app.include_router(addresses_router)
app.include_router(orders_router)
app.include_router(reviews_router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "status_code": exc.status_code, "message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    field_name = first_error["loc"][-1]
    error_msg = first_error.get("msg", "Invalid input")
    message = f"{field_name}: {error_msg}"
    return JSONResponse(
        status_code=422,
        content={"error": True, "status_code": 422, "message": message},
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
    )

    error_response_schema = {
        "type": "object",
        "properties": {
            "error": {"type": "boolean", "example": True},
            "status_code": {"type": "integer", "example": 422},
            "message": {"type": "string", "example": "field_name: Field required"},
        },
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "422" in method.get("responses", {}):
                method["responses"]["422"] = {
                    "description": "Validation Error",
                    "content": {"application/json": {"schema": error_response_schema}},
                }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi