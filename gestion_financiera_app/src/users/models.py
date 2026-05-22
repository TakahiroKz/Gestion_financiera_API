from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean, String

from src.core.base import Base, TimestampMixin, UUIDMixin

class User(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "users"

    username : Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        default=True
    )
    is_verified: Mapped[bool] = mapped_column(
        default=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id")
    )
    role: Mapped["Role"] = relationship(
        back_populates="users"
    )