from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import Activity as ActivitySQL



class Activity(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        from_attributes = True


class ActivityCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

    @staticmethod
    def validate_parent_level(db: Session, parent_id: Optional[int]):
        level = 0
        current_parent = db.query(ActivitySQL).filter(ActivitySQL.id == parent_id).first()
        while current_parent:
            level += 1
            if level >= 3:
                raise HTTPException(status_code=404, detail=f"The maximum level of nesting of activities is 3 levels")
            current_parent = db.query(ActivitySQL).filter(ActivitySQL.id == current_parent.parent_id).first()
