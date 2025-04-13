from sqlalchemy import Column, String, Integer, BIGINT, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BotLog(Base):
    __tablename__ = "bot_logs"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BIGINT, nullable=True)
    test_theme = Column(String, nullable=False)
    test_name = Column(String, nullable=False)
    generation_time = Column(Integer, nullable=False)
    question_num = Column(Integer, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
