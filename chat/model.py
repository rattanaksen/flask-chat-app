from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///chat.db', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all()
    new_user = User(first_name="Skywalker", last_name="Luke",
                    email="lukeskywalker@outlook.com", password="1203")

    session.add(new_user)
    session.commit()