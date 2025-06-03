import logging
from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Configure logging
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create rate limit strings
LOGIN_RATE_LIMIT = "5/minute"
REGISTER_RATE_LIMIT = "3/minute"

# Create rate limit decorators
login_limit = limiter.limit(LOGIN_RATE_LIMIT)
register_limit = limiter.limit(REGISTER_RATE_LIMIT)

# Export the limiter and decorators for use in routes
__all__ = ['limiter', 'login_limit', 'register_limit']

async def rate_limit_middleware(request: Request, call_next):
    """Middleware to apply rate limiting."""
    try:
        # Apply rate limits based on the request path
        if request.url.path == "/auth/login":
            login_limit(request)
        elif request.url.path == "/auth/register":
            register_limit(request)
        
        # Call the next middleware/route handler
        response = await call_next(request)
        return response
        
    except RateLimitExceeded as e:
        logger.warning(f"Rate limit exceeded for {request.url.path}")
        raise HTTPException(status_code=429, detail="Too many requests")
    except Exception as e:
        logger.error(f"Error in rate limit middleware: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
 