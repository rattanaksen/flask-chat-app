from sqlalchemy import create_engine, Column, Integer, String, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

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
    password_hash = Column(String)

    def __iter__(self):
        return iter((self.email, self.password))

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JwtToken(Base):
    __tablename__ = "jwttoken"
    id = Column(Integer, primary_key=True)
    jwt_token = Column(String)

    def get_jwt(self):
        return self.jwt_token


if __name__ == "__main__":
    Base.metadata.create_all()
