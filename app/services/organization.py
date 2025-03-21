from typing import Type

from fastapi import HTTPException
from geopy.distance import distance
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.dto.organization import OrganizationCreate
from app.models import Activity, Building, Organization


def create_organization(org: OrganizationCreate, db: Session):
    org_data = org.dict()
    activity_ids = org_data.pop("activity_ids", [])

    db_org = Organization(**org_data)
    db.add(db_org)
    db.commit()

    for activity_id in activity_ids:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if activity:
            db_org.activities.append(activity)
        else:
            raise ValueError(f"Activity with ID {activity_id} not found")

    db.commit()
    db.refresh(db_org)
    return db_org


def get_organization_by_id(org_id: int, db: Session) -> Type[Organization]:
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return org


def list_organizations(db: Session):
    return db.query(Organization).all()


def delete_organization(org_id: int, db: Session):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(org)
    db.commit()
    return {"detail": "Organization deleted"}


def get_organizations_by_building(building_id: int, db: Session):
    return db.query(Organization).filter(Organization.building_id == building_id).all()


def get_organizations_by_activity(activity_id: int, db: Session):
    return db.query(Organization).join(Organization.activities).filter(Activity.id == activity_id).all()


def get_organizations_by_area(lat: float, lon: float, radius: float,
                              min_lat: float, max_lat: float,
                              min_lon: float, max_lon: float,
                              db: Session):
    query = db.query(Organization).join(Building)
    if radius:
        buildings = db.query(Building).all()
        buildings_in_radius = [b.id for b in buildings if distance((lat, lon), (b.latitude, b.longitude)).km <= radius]
        query = query.filter(Organization.building_id.in_(buildings_in_radius))
    elif all([min_lat, max_lat, min_lon, max_lon]):
        query = query.filter(
            and_(Building.latitude.between(min_lat, max_lat), Building.longitude.between(min_lon, max_lon))
        )
    return query.all()


def search_organization_by_name(name: str, db: Session) -> list[Type[Organization]]:
    return db.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()


def get_organizations_by_activity_tree(activity_id: int, db: Session):
    def get_subactivities(activity_id):
        subactivities = db.query(Activity).filter(Activity.parent_id == activity_id).all()
        return [a.id for a in subactivities] + sum((get_subactivities(a.id) for a in subactivities), [])

    all_activity_ids = [activity_id] + get_subactivities(activity_id)
    return db.query(Organization).join(Organization.activities).filter(Activity.id.in_(all_activity_ids)).all()
