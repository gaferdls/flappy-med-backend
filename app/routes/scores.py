import time

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..db import get_db

router = APIRouter()

MAX_REASONABLE_SCORE = 1000
SUBMIT_COOLDOWN_SECONDS = 2.0

_last_submission_by_player: dict[str, float] = {}


@router.post("/", response_model=schemas.SubmitScoreResponse)
def submit_score(
    data: schemas.ScoreCreate,
    db: Session = Depends(get_db),
) -> schemas.SubmitScoreResponse:
    player_exists = (
        db.query(models.Player).filter(models.Player.id == data.player_id).first()
    )

    if player_exists is None:
        raise HTTPException(status_code=404, detail="Player not found")

    if data.score < 0 or data.score > MAX_REASONABLE_SCORE:
        raise HTTPException(status_code=400, detail="Invalid score")

    now = time.time()
    last_submit = _last_submission_by_player.get(data.player_id)

    if last_submit is not None and (now - last_submit) < SUBMIT_COOLDOWN_SECONDS:
        raise HTTPException(status_code=429, detail="Too many requests")

    _last_submission_by_player[data.player_id] = now

    personal_best = crud.create_score(
        db=db,
        player_id=data.player_id,
        score=data.score,
    )

    return schemas.SubmitScoreResponse(ok=True, personal_best=personal_best)


@router.get("/leaderboard", response_model=schemas.LeaderboardResponse)
def leaderboard(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> schemas.LeaderboardResponse:
    items = crud.get_leaderboard(db=db, limit=limit)
    return schemas.LeaderboardResponse(items=items)

@router.delete("/player/{player_id}")
def delete_player_scores(
    player_id: str,
    db: Session = Depends(get_db),
):
    deleted = db.query(models.Score).filter(
        models.Score.player_id == player_id
    ).delete()

    db.commit()

    return {"deleted": deleted}