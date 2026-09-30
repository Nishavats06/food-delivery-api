VALIDATION_ERROR_RESPONSE = {
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 422},
                        "message": {"type": "string", "example": "field_name: Field required"},
                    },
                }
            }
        },
    }
}

UNAUTHORIZED_RESPONSE = {
    401: {
        "description": "Not authenticated",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 401},
                        "message": {"type": "string", "example": "Not authenticated"},
                    },
                }
            }
        },
    }
}

FORBIDDEN_RESPONSE = {
    403: {
        "description": "Not authorized to perform this action",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 403},
                        "message": {"type": "string", "example": "Only restaurant owners can perform this action"},
                    },
                }
            }
        },
    }
}

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Resource not found",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {"type": "string", "example": "Resource not found"},
                    },
                }
            }
        },
    }
}