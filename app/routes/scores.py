from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..db import get_db

router = APIRouter()

@router.post("/", response_model = schemas.SubmitScoreResponse)
def submit_score(
    data: schemas.ScoreCreate,
    db: Session = Depends(get_db),
) -> schemas.SubmitScoreResponse:
    player_exist = (
        db.query(models.Player).filter(models.Player.id == data.player_id).first()
    )
    
    if player_exist is None:
        raise HTTPException(status_code = 404, detail = "Player not found")

    personal_best = crud.create_score(
        db = db,
        player_id = data.player_id,
        score = data.score,
    )
    return schemas.SubmitScoreResponse(
        ok = True,
        personal_best = personal_best,
    )

@router.get("/leaderboard", response_model = schemas.LeaderboardResponse)
def leaderboard(
    limit: int = Query(default = 10, ge = 1, le = 100),
    db: Session = Depends(get_db),
) -> schemas.LeaderboardResponse:
    items = crud.get_leaderboard(db = db, limit = limit)
    return schemas.LeaderboardResponse(items = items)