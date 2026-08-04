from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import containers, errors
from routers import logs

app = FastAPI(title="Miniwhale API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(containers.router)
app.include_router(logs.router)
app.include_router(errors.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "miniwhale-api"}
