from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import contextmanager
from sqlalchemy import create_engine
from datetime import datetime

#v1
Base = declarative_base()

class Role(Base):

  __tablename__ = "role"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(100))
  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, default=datetime.now())

  user = relationship('User', uselist=False, back_populates='role')
  group_permission = relationship("GroupPermission", back_populates="role")

  def __str__(self):
    return self.name

class User(Base):

  __tablename__ = "user"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(100))
  role_id = Column(Integer, ForeignKey(Role.id), nullable=True)
  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, default=datetime.now())

  role = relationship('Role', uselist=False, back_populates='user')

  def __str__(self):
    data = {"id": self.id, "name": self.name, "role_id": self.role_id}
    return data

class Permission(Base):

  __tablename__ = "permission"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(100))
  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, default=datetime.now())

  group_permission = relationship("GroupPermission", back_populates="permission")

  def __str__(self):
    return self.name
  
class GroupPermission(Base):

  __tablename__ = "group_permission"

  id = Column(Integer, primary_key=True, autoincrement=True)
  role_id = Column(Integer, ForeignKey(Role.id), nullable=True)
  permission_id = Column(Integer, ForeignKey(Permission.id), nullable=True)
  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, default=datetime.now())

  role = relationship("Role", back_populates="group_permission")
  permission = relationship("Permission", back_populates="group_permission")

  def __str__(self):
    return self.name
  

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'Root_12345'
host = 'localhost'
database = 'demo_python_connect_db'

def get_connection():
  return create_engine(
    url="mysql+pymysql://{0}:{1}@{2}/{3}".format(
        user, password, host, database
    )
  )

engine = get_connection()
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
  try:
      Base.metadata.create_all(engine)
      print(
          f"Connection to the {host} for user {user} created successfully.")
  except Exception as ex:
      print("Connection could not be made due to the following error: \n", ex)

