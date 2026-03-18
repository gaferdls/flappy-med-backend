from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db

router = APIRouter()

@router.post("/register", response_model = schemas.RegisterPlayerResponse)
def register_player(
    data: schemas.PlayerRegister,
    db: Session = Depends(get_db),
) -> schemas.RegisterPlayerResponse:
    player = crud.register_player(
        db = db,
        player_id = data.player_id,
        display_name = data.display_name,
    )
    return schemas.RegisterPlayerResponse(
        ok = True,
        player_id = player.id,
        display_name = player.display_name,
    )
