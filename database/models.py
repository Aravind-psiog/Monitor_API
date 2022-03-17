from sqlalchemy import Column, ForeignKey, Integer, String, BOOLEAN, TIMESTAMP
from database.database import Base
from sqlalchemy.orm import relationship


class UserItems(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    created_on = Column(TIMESTAMP)

    group = relationship("GroupItems", back_populates="owner")


class GroupItems(Base):
    __tablename__ = "server_member"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"), unique=False)
    server_group = Column(String)
    admin = Column(BOOLEAN)
    username = Column(String)
    created_on = Column(TIMESTAMP)

    owner = relationship("UserItems", back_populates="group")


class ServerGroup(Base):
    __tablename__ = "server_group"

    server_group = Column(String, primary_key=True, index=True)
    created_on = Column(TIMESTAMP)


class InviteItems(Base):
    __tablename__ = "invite_member"

    id = Column(Integer, primary_key=True, index=True)
    invited_by = Column(String)
    user = Column(String, unique=False, index=True)
    invited_to = Column(String)
    code = Column(String)
    invited_on = Column(TIMESTAMP)


class ServerItems(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    server_group = Column(String, unique=False, index=True)
    created_by = Column(String)
    online = Column(BOOLEAN)
    ip_address = Column(String)
    notified = Column(BOOLEAN, default=False)
