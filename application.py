from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Catalog, Category, CategoryItem

app = Flask(__name__)

#engine = create_engine('sqlite:///catalog.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()

@app.route('/')
@app.route('/catalog/')
def showCatalog():
	#return "This page will show the Catalog"
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/new/')
def newCategory():
	#return "New Category Page"
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showCategory(category_name):
	#return "This page will show the Category Items of: %s" % category_name
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/<string:category_name>/edit/')
def editCategory(category_name):
	#return "Edit Category name of: %s" % category_name
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/<string:category_name>/delete/')
def deleteCategory(category_name):
	#return "Delete Category of: %s" % category_name
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/<string:category_name>/new/')
@app.route('/catalog/<string:category_name>/items/new/')
def newCategoryItem(category_name):
	#return "New Category Item of: %s" % category_name
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showCategoryItem(category_name, item_name):
	#return "Page shows description of item: %s" % item_name
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/<string:category_name>/<string:item_name>/edit/')
def editCategoryItem(category_name, item_name):
	#return "Edit category item of: %s" % item_name
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/catalog/<string:category_name>/<string:item_name>/delete/')
def deleteCategoryItem(category_name, item_name):
	#return "delete category item of: %s" % item_name
	return render_template('restaurants.html', restaurants=restaurants)

if __name__ == '__main__':
	 app.debug = True
	 app.run(host='0.0.0.0', port = 8000)