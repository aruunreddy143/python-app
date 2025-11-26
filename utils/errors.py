import httpx
from fastapi import HTTPException


class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def handle_external_api_error(error: Exception) -> HTTPException:
    """
    Convert external API errors to FastAPI HTTPExceptions.
    Handles httpx and generic exceptions.
    """
    if isinstance(error, httpx.TimeoutException):
        return HTTPException(status_code=504, detail="Request timed out")
    
    elif isinstance(error, httpx.HTTPStatusError):
        return HTTPException(
            status_code=error.response.status_code,
            detail=f"External API error: {error.response.status_code}"
        )
    
    elif isinstance(error, httpx.RequestError):
        return HTTPException(status_code=503, detail="Failed to connect to external API")
    
    else:
        return HTTPException(status_code=500, detail="Unexpected error occurred")
