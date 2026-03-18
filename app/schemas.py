from pydantic import BaseModel, Field


class PlayerRegister(BaseModel):
    player_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1, max_length=12)


class ScoreCreate(BaseModel):
    player_id: str = Field(min_length=1)
    score: int = Field(ge=0, le=100000)


class RegisterPlayerResponse(BaseModel):
    ok: bool
    player_id: str
    display_name: str


class SubmitScoreResponse(BaseModel):
    ok: bool
    personal_best: int


class LeaderboardItem(BaseModel):
    rank: int
    player_id: str
    display_name: str
    score: int


class LeaderboardResponse(BaseModel):
    items: list[LeaderboardItem]