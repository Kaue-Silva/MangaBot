from sqlalchemy import create_engine
from .models import Base
from sqlalchemy.orm import sessionmaker


class DB:
    def __init__(self) -> None:
        engine = create_engine("sqlite:///db.db", echo=True)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    @property
    def get_session(self):
        return self.session

    def close(self):
        self.session.close()
