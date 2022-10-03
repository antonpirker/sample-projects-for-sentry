from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Show(Base):
    __tablename__ = "show_show"

    id = Column(Integer, primary_key=True, index=True)

    show_type = Column(String, index=True)
    title = Column(String, index=True)
    director = Column(String, index=False)
    cast = Column(String, index=False)
    countries = Column(String, index=False)
    date_added = Column(String, index=False)
    rating = Column(String, index=False)
    duration = Column(String, index=False)
    categories = Column(String, index=False)
    description = Column(String, index=False)
    release_year = Column(Integer)
