# app/models/app_config.py
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class AppConfig(Base):
    __tablename__ = "app_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    registration_count: Mapped[int] = mapped_column(Integer, default=0)
    login_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    launch_message: Mapped[str] = mapped_column(
        String, default="Launching soon"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )