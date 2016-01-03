import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

   id = Column(Integer, primary_key=True)
   name = Column(String(250), nullable=False)
   email = Column(String(250), nullable=False)
   picture = Column(String(250))

class Section(Base):
    __tablename__ = 'section'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    sectionItems = relationship("SectionItem", cascade="all, delete-orphan")

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'user_id'      : self.user_id
       }


class SectionItem(Base):
    __tablename__ = 'section_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category = Column(String(250))
    section_id = Column(Integer, ForeignKey('section.id'))
    section = relationship(Section)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         	: self.name,
           'description'   : self.description,
           'id'         	: self.id,
           'category'      : self.category,
       }

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
