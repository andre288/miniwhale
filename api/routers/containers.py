from fastapi import APIRouter, HTTPException
from services.docker import get_containers

router = APIRouter(prefix="/containers", tags=["containers"])


@router.get("/")
def list_containers():
    try:
        containers = get_containers()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Get containers error: {e}")

    return {"containers": containers}
