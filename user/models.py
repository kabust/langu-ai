from sqlalchemy import Column, Integer, String

from database import Base


class DBUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone = Column(String(255))
    thread_id = Column(String(255))

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
