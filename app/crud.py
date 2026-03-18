from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models

def register_player(db: Session, player_id: str, display_name: str) -> models.Player:
    player = db.query(models.Player).filter(models.Player.id == player_id).first()

    if player is None:
        player = models.Player(id = player_id, display_name = display_name)
        db.add(player)
    else:
        player.display_name = display_name
        
    db.commit()
    db.refresh(player)
    return player
    
def create_score(db: Session, player_id: str, score: int) -> int:
    db_score = models.Score(player_id = player_id, score = score)
    db.add(db_score)
    db.commit()
    
    personal_best = (
        db.query(func.max(models.Score.score))
        .filter(models.Score.player_id == player_id)
        .scalar()
    )
    
    return int(personal_best or 0)

def get_leaderboard(db: Session, limit: int = 10) -> list[dict]:
    rows = (
        db.query(
            models.Player.display_name.label("display_name"),
            func.max(models.Score.score).label("score"),
        )
        .join(models.Score, models.Score.player_id == models.Player.id)
        .group_by(models.Player.id, models.Player.display_name)
        .order_by(func.max(models.Score.score).desc(), models.Player.display_name.asc())
        .limit(limit)
        .all()
    )

    items: list[dict] = []
    for index, row in enumerate(rows, start = 1):
        items.append(
            {
                "rank": index,
                "display_name": row.display_name,
                "score": int(row.score),
            }
        )
    return items