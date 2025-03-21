from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dto.activity import ActivityCreate
from app.models import Activity


def create_activity(activity: ActivityCreate, db: Session):
    if activity.parent_id:
        parent_exists = db.query(Activity).filter(Activity.id == activity.parent_id).first()
        if not parent_exists or activity.parent_id == 0:
            raise HTTPException(status_code=404, detail=f"Parent activity with ID {activity.parent_id} does not exist")

        ActivityCreate.validate_parent_level(db, activity.parent_id)

    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def read_activity(activity_id: int, db: Session):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


def list_activities(db: Session):
    return db.query(Activity).all()


def delete_activity(activity_id: int, db: Session):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.query(Activity).filter(Activity.parent_id == activity_id).update({"parent_id": activity.parent_id})

    db.delete(activity)
    db.commit()
    return {"detail": "Activity deleted"}
