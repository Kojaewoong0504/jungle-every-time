from sqlalchemy.orm import Session
from src.app.models.models import User


async def get_user_by_id(db: Session, input_id: int):
    #  amazonq-ignore-next-line
    return db.query(User).filter(User.id == input_id).first()
