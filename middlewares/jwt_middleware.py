from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt

SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ALGORITHM = "HS256"  # Replace with the algorithm used to sign the token


class JWTMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate JWT tokens in the Authorization header.
    """

    async def dispatch(self, request: Request, call_next):
        # Extract the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing or invalid"},
            )

        # Extract the token
        token = auth_header.split(" ")[1]
        try:
            # Decode and verify the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload  # Attach the decoded payload to the request
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401, content={"detail": "Token has expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        # Proceed to the next middleware or route handler
        return await call_next(request)
