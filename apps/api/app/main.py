from fastapi import FastAPI

from v1.logic.scheduler.scheduler import lifespan
from v1.routers import router as v1_router

app = FastAPI(
    lifespan=lifespan
)
app.include_router(v1_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)