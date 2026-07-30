from fastapi import HTTPException, APIRouter, Request
from fastapi.responses import StreamingResponse
from services.docker import get_logs, generate_logs
import aiodocker
from exceptions import ContainerNotFoundError

router = APIRouter(prefix="/container/{container_id}", tags=["logs"])

@router.get("/logs")
def get_container_log(container_id: str):
    
    try:
        logs = get_logs(container_id)

    except ContainerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return logs


@router.get("/logs/stream")
async def stream_logs(container_id: str, request: Request):
    client = aiodocker.Docker()
    try:
        await client.containers.get(container_id)
    except aiodocker.exceptions.DockerContainerError as e:
        await client.close()
        if e.status == 404:
            raise HTTPException(status_code=404, detail=f"Container {container_id} not found")
        raise HTTPException(status_code=500, detail=e.message)
    return StreamingResponse(generate_logs(client, container_id, request), media_type="text/plain")
