from fastapi import FastAPI

from . import models
from .db import engine
from .routes import players, scores

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flappy Med Backend")

@app.get("/")
def root():
    return {"message": "Flappy Med Backend Running"}

@app.get("/")
def root() -> dict[str, str]:
    return {"status": "Flappy Med Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(scores.router, prefix="/scores", tags=["scores"])