from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    energy = Column(Integer, default=100)

    str = Column(Integer, default=5)
    agi = Column(Integer, default=5)
    lck = Column(Integer, default=5)
    end = Column(Integer, default=5)
    int = Column(Integer, default=5)

    gold = Column(Integer, default=5000)
    pills = Column(Integer, default=1000)
    bucks = Column(Integer, default=50)

    bandage_count = Column(Integer, default=5)
    medkit_count = Column(Integer, default=3)
    energy_drink_count = Column(Integer, default=3)

    # JSON‑поле для хранения списка купленных предметов
    purchased_items = Column(JSON, nullable=True)

    lifesteal = Column(Float, default=0.0)
    regen = Column(Float, default=0.0)

    stat_points_unspent = Column(Integer, default=0)

    battle_state = Column(String, default="idle")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # связь с User
    user = relationship("User", backref="character", uselist=False)
