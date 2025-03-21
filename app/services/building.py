from fastapi import HTTPException
from geopy.distance import distance
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.dto.building import BuildingCreate
from app.models import Building


def create_building(building: BuildingCreate, db: Session):
    db_building = Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


def read_building(building_id: int, db: Session):
    building = db.query(Building).filter(Building.id == building_id).first()
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


def list_buildings(db: Session):
    return db.query(Building).all()


def delete_building(building_id: int, db: Session):
    building = db.query(Building).filter(Building.id == building_id).first()
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    db.delete(building)
    db.commit()
    return {"detail": "Building deleted"}


def get_buildings_by_area(lat: float, lon: float, radius: float, min_lat: float, max_lat: float, min_lon: float,
                          max_lon: float, db: Session):
    query = db.query(Building)
    if radius:
        buildings = db.query(Building).all()
        buildings_in_radius = [b for b in buildings if distance((lat, lon), (b.latitude, b.longitude)).km <= radius]
        query = query.filter(Building.id.in_([b.id for b in buildings_in_radius]))
    elif all([min_lat, max_lat, min_lon, max_lon]):
        query = query.filter(
            and_(Building.latitude.between(min_lat, max_lat), Building.longitude.between(min_lon, max_lon))
        )
    return query.all()
