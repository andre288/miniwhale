from fastapi import APIRouter

router = APIRouter(prefix="/errors", tags=["errors"])


@router.get("/")
def list_errors():
    # Placeholder — real implementation will return grouped, AI-analyzed errors
    return {"errors": []}
