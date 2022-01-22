from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property()


class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    player = Column(String, nullable=False)
    points = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.player}\t{self.points}'


def create():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
