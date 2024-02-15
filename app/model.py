from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class BaseModel(db.Modle):
  __abstract__ = True

  id = Column(Integer, primary_key=True, autoincrement=True)

class Role (BaseModel):
  __tablename__ = "role"

  name = Column(String, nullable=False)

  def __str__(self):
    return self.name
  
class User (BaseModel):
  __tablename__ = "user"

  name = Column(String, nullable=False)
  roleId = Column(Integer, ForeignKey(Role.id))
  role = relationship('Role', backref='user', lazy=True)

  def __str__(self):
    return self.name
  

if __name__ == "__main__":
  db.create_all()
