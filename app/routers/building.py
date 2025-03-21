from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dto.building import Building as BuildingDTO, BuildingCreate
from app.services import building as BuildingService

router = APIRouter()


@router.post("/buildings/", response_model=BuildingDTO, tags=['buildings'])
def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
    """
        Создать новое здание.

        Этот метод создает новое здание на основе данных, переданных в запросе.

        Возвращает созданное здание.
        """
    return BuildingService.create_building(building=building, db=db)


@router.get("/buildings/by-area", response_model=list[BuildingDTO], tags=['buildings'])
def get_buildings_by_area(lat: float, lon: float, radius: float = Query(None),
                          min_lat: float = Query(None), max_lat: float = Query(None),
                          min_lon: float = Query(None), max_lon: float = Query(None),
                          db: Session = Depends(get_db)):
    """
        Получить здания по географической области.

        Этот метод возвращает список зданий, находящихся в пределах указанной области.
        Область может быть задана либо радиусом вокруг точки, либо прямоугольником.

        - **lat**: Широта центра области.
        - **lon**: Долгота центра области.
        - **radius**: Радиус поиска в километрах (опционально).
        - **min_lat**: Минимальная широта (опционально).
        - **max_lat**: Максимальная широта (опционально).
        - **min_lon**: Минимальная долгота (опционально).
        - **max_lon**: Максимальная долгота (опционально).

        Возвращает список зданий.
        """
    return BuildingService.get_buildings_by_area(lat=lat, lon=lon, radius=radius, min_lat=min_lat,
                                                 max_lat=max_lat, min_lon=min_lon, max_lon=max_lon, db=db)


@router.get("/buildings/{building_id}", response_model=BuildingDTO, tags=['buildings'])
def read_building(building_id: int, db: Session = Depends(get_db)):
    """
        Получить здание по ID.

        Этот метод возвращает здание с указанным ID.
        Если здание не найдено, возвращается ошибка 404.

        - **building_id**: ID здания.

        Возвращает здание.
        """
    return BuildingService.read_building(building_id=building_id, db=db)


@router.get("/buildings/", response_model=list[BuildingDTO], tags=['buildings'])
def list_buildings(db: Session = Depends(get_db)):
    """
        Получить список всех зданий.

        Этот метод возвращает список всех зданий, зарегистрированных в системе.

        Возвращает список зданий.
        """
    return BuildingService.list_buildings(db=db)


@router.delete("/buildings/{building_id}", tags=['buildings'])
def delete_building(building_id: int, db: Session = Depends(get_db)):
    """
        Удалить здание по ID.

        Этот метод удаляет здание с указанным ID.
        Если здание не найдено, возвращается ошибка 404.

        - **building_id**: ID здания.

        Возвращает сообщение об успешном удалении.
        """
    return BuildingService.delete_building(building_id=building_id, db=db)
