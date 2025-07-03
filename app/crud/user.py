from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserAddress
from sqlalchemy.exc import SQLAlchemyError

class UserCRUD:

    @staticmethod
    async def create_user(
            db: AsyncSession,
            first_name: str,
            last_name: str,
            number: str
    ):
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                number=number
            )
            db.add(user)
            await db.commit()
            return user
        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error: {str(e)}"}
        except Exception as e:
            await db.rollback()
            return {"error": f"Unexpected error: {str(e)}"}


