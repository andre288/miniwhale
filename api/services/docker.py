# https://github.com/docker/docker-py

import docker
import aiodocker
from fastapi import Request
from exceptions import ContainerNotFoundError
import asyncio
try:
    client = docker.from_env()
except docker.errors.APIError as e:
    raise Exception(f"Docker socket connection error: {e}")


def get_containers():
    containers = client.containers.list()

    return [
        {
            "short_id": c.short_id,
            "name": c.name,
            "status": c.status,
        } for c in containers
        ]


def get_logs(container_id):

    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=20).decode("utf-8")

    except docker.errors.NotFound:
        raise ContainerNotFoundError(container_id)

    return {
            "short_id": container.short_id,
            "name": container.name, 
            "logs": logs
        }


async def generate_logs(client, container_id: str, request: Request):
    try:
        container = client.containers.container(container_id)
        log_stream = container.log(stdout=True, stderr=True, follow=True).__aiter__()

        while True:
            if await request.is_disconnected():
                break
            try:
                line = await asyncio.wait_for(log_stream.__anext__(), timeout=0.1)
            except asyncio.TimeoutError:
                # nada de novo em 15s — manda um "heartbeat" e checa de novo
                yield ""
                continue
            except StopAsyncIteration:
                # o stream de logs terminou (container parou, por exemplo)
                break

            yield line

    except aiodocker.exceptions.DockerError as e:
        yield f"error: {str(e)}"
    finally:
        await client.close()