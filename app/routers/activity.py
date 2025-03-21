from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dto.activity import Activity as ActivityDTO, ActivityCreate
from app.services import activity as ActivityService

router = APIRouter()


@router.post("/activities/", response_model=ActivityDTO, tags=['activities'])
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """
        Создать новую деятельность.

        Этот метод создает новую деятельность на основе данных, переданных в запросе.

        Возвращает созданную деятельность.
        """
    return ActivityService.create_activity(activity=activity, db=db)


@router.get("/activities/{activity_id}", response_model=ActivityDTO, tags=['activities'])
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    """
        Получить деятельность по ID.

        Этот метод возвращает деятельность с указанным ID.
        Если деятельность не найдена, возвращается ошибка 404.

        - **activity_id**: ID деятельности.

        Возвращает деятельность.
        """
    return ActivityService.read_activity(activity_id=activity_id, db=db)


@router.get("/activities/", response_model=list[ActivityDTO], tags=['activities'])
def list_activities(db: Session = Depends(get_db)):
    """
        Получить список всех деятельностей.

        Этот метод возвращает список всех деятельностей, зарегистрированных в системе.

        Возвращает список деятельностей.
        """
    return ActivityService.list_activities(db=db)


@router.delete("/activities/{activity_id}", tags=['activities'])
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """
        Удалить деятельность по ID.

        Этот метод удаляет деятельность с указанным ID.
        Если деятельность не найдена, возвращается ошибка 404.

        - **activity_id**: ID деятельности.

        Возвращает сообщение об успешном удалении.
        """
    return ActivityService.delete_activity(activity_id=activity_id, db=db)
