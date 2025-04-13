from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import BotLog
from sqlalchemy import exc


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


class BotLogsRepository(BaseRepository):
    async def add_log(self, info: dict) -> None:
        try:
            user_db = BotLog(
                user_id=info["user_id"],
                test_theme=info["test_theme"],
                test_name=info["test_name"],
                generation_time=info["generation_time"],
                question_num=info["question_num"],
                date=info["date"],
            )
            self.session.add(user_db)
            await self.session.commit()
            return user_db.id
        except exc.SQLAlchemyError as e:
            await self.session.rollback()
            raise e
