from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Show Catalog
@app.route('/')
@app.route('/catalog/')
def showCatalog():
	categorys = session.query(Category).all()
	return render_template('catalog.html', categorys = categorys)


#Create new Category
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
	if request.method == 'POST':
		  newCategory = Category(name=request.form['name'], description=request.form['description'])
		  session.add(newCategory)
		  session.commit()
		  return redirect(url_for('showCatalog'))
	else:
		  return render_template('newcategory.html')	


#Show category items
@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/items/')
def showCategory(category_name):
	category = session.query(Category).filter_by(name=category_name).one()
	category_id = category.id
	items= session.query(CategoryItem).filter_by(category_id = category_id).all()
	return render_template('category.html', category = category, items=items)	


#Edit category name
@app.route('/catalog/<category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
	editedCategory = session.query(Category).filter_by(name=category_name).one()
	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name = request.form['name']
		if request.form['description']:
			editedCategory.description = request.form['description']
		session.add(editedCategory)
		session.commit()
		return redirect(url_for('showCatalog'))
	else:
		return render_template('editcategory.html', category = editedCategory)	


#Delete category
@app.route('/catalog/<category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
	categoryToDelete = session.query(Category).filter_by(name=category_name).one()
	if request.method == 'POST':
		session.delete(categoryToDelete)
		session.commit()
		return redirect(url_for('showCatalog'))
	else:
		return render_template('deletecategory.html', category = categoryToDelete)	


#Create new category item
@app.route('/catalog/<category_name>/new/', methods=['GET', 'POST'])
@app.route('/catalog/<category_name>/items/new/', methods=['GET', 'POST'])
def newCategoryItem(category_name):
	category = session.query(Category).filter_by(name=category_name).one()
	category_id = category.id
	if request.method == 'POST':
		newItem = CategoryItem(name=request.form['name'], description=request.form['description'],
									  category_id=category_id)
		session.add(newItem)
		session.commit()

		return redirect(url_for('showCategory', category_name=category_name))
	else:
		return render_template('newitem.html', category_name = category_name)	


#Look at category item
@app.route('/catalog/<category_name>/<item_name>/')
def showCategoryItem(category_name, item_name):
	category = session.query(Category).filter_by(name=category_name).one()
	item = session.query(CategoryItem).filter_by(name=item_name).one()
	return render_template('item.html', item=item, category=category)


#Edit category item
@app.route('/catalog/<category_name>/<item_name>/edit/', methods=['GET', 'POST'])
def editCategoryItem(category_name, item_name):
	editedItem = session.query(CategoryItem).filter_by(name=item_name).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('showCategory', category_name=category_name))
	else:
		return render_template('edititem.html', category_name=category_name, item_name=item_name, item=editedItem)


#Delete category item
@app.route('/catalog/<category_name>/<item_name>/delete/', methods=['GET', 'POST'])
def deleteCategoryItem(category_name, item_name):
	itemToDelete = session.query(CategoryItem).filter_by(name=item_name).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('showCategory', category_name=category_name))
	else:
		return render_template('deleteitem.html', category_name=category_name, item_name=item_name, item=itemToDelete)

if __name__ == '__main__':
	 app.debug = True
	 app.run(host='0.0.0.0', port = 8000)