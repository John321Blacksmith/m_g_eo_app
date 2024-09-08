# validation of the objects is done here

from pydantic import BaseModel


class CityInterface(BaseModel):
    """
    Validate request & response
    data of the city object.
    """
    name: str
    latitude: float
    longitude: float