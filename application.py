from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CategoryItem

#Fake Categories
category = {'name':'Soccer', 'description':'Football match', 'id': '1'}
categorys = [ {'name':'Soccer', 'description':'Football match','id':'1'}, {'name':'Basketball', 'description':'Basketball match','id':'2'},{'name':'Baseball', 'description':'Baseball match','id':'3'},{'name':'Frisbee', 'description':'Frisbee match','id':'4'} ]

#Fake Items
item =  {'name':'Arsenal', 'description':'Arsenal team'}
items = [ {'name':'Arsenal', 'description':'Arsenal team', 'id': '1'}, {'name':'Man United', 'description':'Man United team','id':'2'},{'name':'Chelsea', 'description':'Chelsea team','id':'3'},{'name':'West Ham', 'description':'West Ham team','id':'4'} ]

app = Flask(__name__)

#engine = create_engine('sqlite:///catalog.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()

#Show Catalog
@app.route('/')
@app.route('/catalog/')
def showCatalog():
	#return "This page will show the Catalog"
	return render_template('catalog.html', categorys = categorys)

#Create new Category
@app.route('/catalog/new/')
def newCategory():
	#return "New Category Page"
	return render_template('newcategory.html')

#Look at items in category
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showCategory(category_name):
	#return "This page will show the Category: %s" % category_name
	return render_template('category.html', category = category, items=items)

#Edit category name
@app.route('/catalog/<string:category_name>/edit/')
def editCategory(category_name):
	#return "Edit Category: %s" % category_name
	return render_template('editcategory.html', category = category)

#Delete category
@app.route('/catalog/<string:category_name>/delete/')
def deleteCategory(category_name):
	#return "Delete Category: %s" % category_name
	return render_template('deletecategory.html', category = category)

#Create new category item
@app.route('/catalog/<string:category_name>/new/')
@app.route('/catalog/<string:category_name>/items/new/')
def newCategoryItem(category_name):
	#return "New Category Item of: %s" % category_name
	return render_template('newitem.html', category = category)

#Look at category item
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showCategoryItem(category_name, item_name):
	#return "Page shows description of item: %s" % item_name
	return render_template('item.html',category_name=category_name, item_name=item_name, item=item, category=category)

#Edit category item
@app.route('/catalog/<string:category_name>/<string:item_name>/edit/')
def editCategoryItem(category_name, item_name):
	#return "Edit category item of: %s" % item_name
	return render_template('edititem.html', category_name=category_name, item_name=item_name, item=item,category=category)

#Delete category item
@app.route('/catalog/<string:category_name>/<string:item_name>/delete/')
def deleteCategoryItem(category_name, item_name):
	#return "delete category item of: %s" % item_name
	return render_template('deleteitem.html', category_name=category_name, item_name=item_name, item=item,category=category)

if __name__ == '__main__':
	 app.debug = True
	 app.run(host='0.0.0.0', port = 8000)