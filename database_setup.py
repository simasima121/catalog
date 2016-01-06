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

class Catalog(Base):
	__tablename__ = 'catalog'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name'         : self.name,
			'id'           : self.id,
			'user_id'      : self.user_id
		}

class Category(Base):
	__tablename__ = 'category'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	catalog_id = Column(Integer, ForeignKey('catalog.id'))
	catalog = relationship(Catalog)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name'         	: self.name,
			'description'    : self.description,
			'id'          	  : self.id,
			'category'       : self.category,
		}

class CategoryItem(Base):
	__tablename__ = 'category_item'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	catalog_id = Column(Integer, ForeignKey('catalog.id'))
	catalog = relationship(Catalog)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
