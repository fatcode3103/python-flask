from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime
from . import get_engine

engine = get_engine()

# v1
Base = declarative_base()


class Role(Base):

    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    user = relationship("User", uselist=False, back_populates="role")
    group_permission = relationship("GroupPermission", back_populates="role")

    def __str__(self):
        data = {"id": self.id, "name": self.name}
        return data


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    role_id = Column(Integer, ForeignKey(Role.id), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    role = relationship("Role", uselist=False, back_populates="user")

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


if __name__ == "__main__":
    try:
        Base.metadata.create_all(engine)
    except Exception as ex:
        print("Something's wrong", ex)
