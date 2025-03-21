from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    children = relationship("Activity", backref="parent", remote_side=[id])


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    organizations = relationship("Organization", back_populates="building")


organization_activity = Table(
    "organization_activity", Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id"))
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_numbers = Column(String, nullable=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity, backref="organizations")
