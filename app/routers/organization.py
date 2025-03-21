from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dto.organization import Organization as OrganizationDTO, OrganizationCreate
from app.services import organization as OrganizationService

router = APIRouter()


@router.post("/organizations/", response_model=OrganizationDTO, tags=['organizations'])
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    """
        Создать новую организацию.

        Этот метод создает новую организацию на основе данных, переданных в запросе.
        Поле `activity_ids` используется для связывания организации с активностями.

        Возвращает созданную организацию.
        """
    return OrganizationService.create_organization(org=org, db=db)


@router.get("/organizations/by-area", response_model=list[OrganizationDTO], tags=['organizations'])
def get_organizations_by_area(lat: float, lon: float, radius: float = Query(None),
                              min_lat: float = Query(None), max_lat: float = Query(None),
                              min_lon: float = Query(None), max_lon: float = Query(None),
                              db: Session = Depends(get_db)):
    """
        Получить организации по географической области.

        Этот метод возвращает список организаций, находящихся в пределах указанной области.
        Область может быть задана либо радиусом вокруг точки, либо прямоугольником.

        - **lat**: Широта центра области.
        - **lon**: Долгота центра области.
        - **radius**: Радиус поиска в километрах (опционально).
        - **min_lat**: Минимальная широта (опционально).
        - **max_lat**: Максимальная широта (опционально).
        - **min_lon**: Минимальная долгота (опционально).
        - **max_lon**: Максимальная долгота (опционально).

        Возвращает список организаций.
        """
    return OrganizationService.get_organizations_by_area(lat=lat, lon=lon, radius=radius, min_lat=min_lat,
                                                         max_lat=max_lat, min_lon=min_lon, max_lon=max_lon, db=db)


@router.get("/organizations/by-name", response_model=list[OrganizationDTO], tags=['organizations'])
def search_organization_by_name(name: str, db: Session = Depends(get_db)):
    """
        Поиск организаций по названию.

        Этот метод возвращает список организаций, название которых содержит указанную строку.

        - **name**: Строка для поиска в названиях организаций.

        Возвращает список организаций.
        """
    return OrganizationService.search_organization_by_name(name=name, db=db)


@router.get("/organizations/{org_id}", response_model=OrganizationDTO, tags=['organizations'])
def get_organization_by_id(org_id: int, db: Session = Depends(get_db)):
    """
        Получить организацию по ID.

        Этот метод возвращает организацию с указанным ID.
        Если организация не найдена, возвращается ошибка 404.

        - **org_id**: ID организации.

        Возвращает организацию.
        """
    return OrganizationService.get_organization_by_id(org_id=org_id, db=db)


@router.get("/organizations/", response_model=list[OrganizationDTO], tags=['organizations'])
def list_organizations(db: Session = Depends(get_db)):
    """
        Получить список всех организаций.

        Этот метод возвращает список всех организаций, зарегистрированных в системе.

        Возвращает список организаций.
        """
    return OrganizationService.list_organizations(db=db)


@router.delete("/organizations/{org_id}", tags=['organizations'])
def delete_organization(org_id: int, db: Session = Depends(get_db)):
    """
        Удалить организацию по ID.

        Этот метод удаляет организацию с указанным ID.
        Если организация не найдена, возвращается ошибка 404.

        - **org_id**: ID организации.

        Возвращает сообщение об успешном удалении.
        """
    return OrganizationService.delete_organization(org_id=org_id, db=db)


@router.get("/organizations/by-building/{building_id}", response_model=list[OrganizationDTO], tags=['organizations'])
def get_organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    """
        Получить организации по ID здания.

        Этот метод возвращает список организаций, связанных с указанным зданием.

        - **building_id**: ID здания.

        Возвращает список организаций.
        """
    return OrganizationService.get_organizations_by_building(building_id=building_id, db=db)


@router.get("/organizations/by-activity/{activity_id}", response_model=list[OrganizationDTO], tags=['organizations'])
def get_organizations_by_activity(activity_id: int, db: Session = Depends(get_db)):
    """
        Получить организации по ID активности.

        Этот метод возвращает список организаций, связанных с указанной активностью.

        - **activity_id**: ID активности.

        Возвращает список организаций.
        """
    return OrganizationService.get_organizations_by_activity(activity_id=activity_id, db=db)


@router.get("/organizations/by-activity-tree/{activity_id}", response_model=list[OrganizationDTO], tags=['organizations'])
def get_organizations_by_activity_tree(activity_id: int, db: Session = Depends(get_db)):
    """
        Получить организации по дереву активностей.

        Этот метод возвращает список организаций, связанных с указанной активностью и её дочерними активностями.

        - **activity_id**: ID активности.
        - **db**: Сессия базы данных.

        Возвращает список организаций.
        """
    return OrganizationService.get_organizations_by_activity_tree(activity_id=activity_id, db=db)
