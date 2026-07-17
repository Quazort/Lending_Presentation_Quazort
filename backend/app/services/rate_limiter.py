from fastapi import Request, HTTPException, status
from backend.app.repositories.rate_limit import rate_limit_repo


async def check_contact_rate_limit(request: Request):
    client_ip = request.client.host

    if rate_limit_repo.is_rate_limited(ip=client_ip, limit=5, window=60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )