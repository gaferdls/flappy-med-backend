from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .db import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(String, primary_key=True, index=True)
    display_name = Column(String(12), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, ForeignKey("players.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)