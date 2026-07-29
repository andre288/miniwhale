from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Miniwhale API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "miniwhale-api"}


@app.get("/containers")
def list_containers():
    # Placeholder — real implementation will query the Docker SDK
    return {"containers": []}


@app.get("/errors")
def list_errors():
    # Placeholder — real implementation will return grouped, AI-analyzed errors
    return {"errors": []}