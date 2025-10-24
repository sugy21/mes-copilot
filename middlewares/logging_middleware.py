import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log request URL and response time.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(
            f"Request URL: {request.url} | Processing Time: {process_time:.4f} seconds"
        )
        return response
