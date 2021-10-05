import random

import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.service.service import DataStore


Base = declarative_base()


class Stat(Base):

    __tablename__ = 'stats'

    id            =   Column(Integer, primary_key=True)
    profile_id    =   Column(String(255))
    resource      =   Column(String(255))
    counts        =   Column(Integer)
    
    def __repr__(self):
        return f"<Stat (profile={self.profile_id}, resource={self.resource}, counts={self.counts})>"


class MySQLDB(DataStore):

    RESOURCE = 'things'

    @classmethod
    def from_dict(cls, data: dict):
        connection_string = f"mysql://{data['USER']}:{data['PASS']}@{data['HOST']}:{data['PORT']}/{data['DB']}"
        engine = db.create_engine(connection_string)
        Base.metadata.create_all(engine)
        return cls(engine)
    
    def __init__(self, engine):
        self._engine = engine

    def get_count(self, profile_id: str):
        with self._engine.connect() as conn:
            Session = sessionmaker(bind=self._engine)
            session = Session()
            with session.begin():
                stat = session.query(Stat).filter(Stat.profile_id == profile_id).first()
                if stat is None:
                    new_count = random.randint(0,50)
                    stat = Stat(
                        profile_id=profile_id,
                        resource=MySQLDB.RESOURCE,
                        counts=new_count
                    )
                    session.add(stat)
                    session.commit()

    def increment_count(self, profile_id: str):
        with self._engine.connect() as conn:
            Session = sessionmaker(bind=self._engine)
            session = Session()
            with session.begin():
                stat = session.query(Stat).filter(Stat.profile_id == profile_id).first()
                if stat is not None:
                    stat.counts = stat.counts + 1
                    session.add(stat)
                    session.commit()

    def decrement_count(self, profile_id: str):
        with self._engine.connect() as conn:
            Session = sessionmaker(bind=self._engine)
            session = Session()
            with session.begin():
                stat = session.query(Stat).filter(Stat.profile_id == profile_id).first()
                if stat is not None:
                    stat.counts = stat.counts - 1
                    session.add(stat)
                    session.commit()
