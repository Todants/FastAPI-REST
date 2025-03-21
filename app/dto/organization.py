from typing import List, Optional

from pydantic import BaseModel

from app.dto.activity import Activity
from app.dto.building import Building


class Organization(BaseModel):
    id: int
    name: str
    phone_numbers: str
    building: Building
    activities: List[Activity]

    class Config:
        from_attributes = True


class OrganizationCreate(BaseModel):
    name: str
    phone_numbers: Optional[str] = None
    building_id: int
    activity_ids: list[int]
