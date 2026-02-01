from fastapi import APIRouter, Request, Response
import httpx
from app.config import AUTH_SERVICE_URL, CONTENT_SERVICE_URL, SEARCH_SERVICE_URL, MEDIA_SERVICE_URL

router = APIRouter()

# Routes mapping the other microservices
SERVICE_MAP = {
    "/auth": AUTH_SERVICE_URL,
    "/notes": CONTENT_SERVICE_URL,
    "/search": SEARCH_SERVICE_URL,
    "/media": MEDIA_SERVICE_URL,
}

# Forward the requests to the corresponding service that needs to handle it
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request):
    incoming_path = "/" + path
    service_url = None

    # Check if the service url is present in the local list of services
    for prefix, base_url in SERVICE_MAP.items():
        if incoming_path.startswith(prefix):
            service_url = base_url
            break

    if not service_url:
        return Response("Service not found", status_code=404)

    url = service_url + incoming_path

    # Forward the headers to the service
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            request.method,
            url,
            headers=headers,
            params=request.query_params,
            content=await request.body(),
            timeout=10.0
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        media_type=resp.headers.get("content-type")
    )
