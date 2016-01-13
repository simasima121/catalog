from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, CategoryItem

engine = create_engine('sqlite:///catalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

#Football Category
category1 = Category(name="Football", description="Football match")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(user_id=1, name="Arsenal", description="Arsenal team", category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Man United", description="Man United team", category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Chelsea", description="Chelsea team", category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="West Ham", description="West Ham team", category=category1)

session.add(categoryItem4)
session.commit()


#Basketball Category
category2 = Category(name="Basketball", description="Basketball match")

session.add(category2)
session.commit()

categoryItem1 = CategoryItem(user_id=1, name="Boston Celtics", description="Boston Celtics team", category=category2)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Dallas Mavericks", description="Dallas Mavericks team", category=category2)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Brooklyn Nets", description="Brooklyn Nets team", category=category2)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Houston Rockets", description="Houston Rockets team", category=category2)

session.add(categoryItem4)
session.commit()

#Baseball Category
category3 = Category(name="Baseball", description="Baseball match")

session.add(category3)
session.commit()

categoryItem1 = CategoryItem(user_id=1, name="Baltimore Orioles", description="Baltimore Orioles team", category=category3)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="New York Yankees", description="New York Yankees	team", category=category3)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Toronto Blue Jays", description="Toronto Blue Jays team", category=category3)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Chicago White Sox", description="Chicago White Sox team", category=category3)

session.add(categoryItem4)
session.commit()

#Frisbee Category
category4 = Category(name="Frisbee", description="Frisbee match")

session.add(category4)
session.commit()

categoryItem1 = CategoryItem(user_id=1, name="AirBadgers", description="AirBadgers team", category=category4)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Devon", description="Devon team", category=category4)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Evolution", description="Evolution team", category=category4)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Red", description="Red team", category=category4)

session.add(categoryItem4)
session.commit()


 
print "added catalog items!"