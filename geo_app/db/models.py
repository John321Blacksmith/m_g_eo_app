# model representation of the city
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Float
from sqlalchemy.orm import mapped_column


class CityBase(DeclarativeBase):
    """
    Base model for all
    the city-like intefaces.
    """
    pass


class City(CityBase):
    """
    Standart city object
    representation.
    """
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    longitude: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return f'City: {self.name}'
    
