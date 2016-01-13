from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

#uses flask session as login_session works as dictonary, stores values for longevity of users access
from flask import session as login_session
import random, string

#stores client secrets
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
#onverts return value from function into real response object that we can send to client
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
	 open('client_secrets.json', 'r').read())['web']['client_id']


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login/')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
						for x in xrange(32))
	login_session['state'] = state
	#return "The current session state is %s" % login_session['state']
	return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data

	# try and use 1 time code in exchange for credentials object
	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
			% access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	#Check to see if user is already logged in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['provider'] = 'google'
	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id
	response =  make_response(json.dumps('Successfully connected user'), 200)

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']


	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("You Are Now Logged In As %s" % login_session['username'])
	print "done!"
	return output


#JSON APIs to view Catalog Info
@app.route('/catalog.json/')
def catalogJSON():
	categorys = session.query(Category).all()
	serializedCategories = []

	for c in categorys:
		new_cat = c.serialize
		items = session.query(CategoryItem).filter_by(category_id = c.id).all()
		serializedItems = []

		for i in items:
			serializedItems.append(i.serialize)
		new_cat['items'] = serializedItems
		serializedCategories.append(new_cat)
		
	return jsonify(Category=[serializedCategories])

#Show Catalog
@app.route('/')
@app.route('/catalog/')
def showCatalog():
	categorys = session.query(Category).all()
	#items = session.query(CategoryItem).order_by(CategoryItem.id.desc()).all()
	items = session.query(CategoryItem).all()
	return render_template('catalog.html', categorys = categorys, items=items)


#Create new Category
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
	exist = False
	if request.method == 'POST':
		categorys = session.query(Category).all()
		for c in categorys:
			category_n = c.name
			if request.form['name'] == category_n:
				exist = True
		if exist == False:
			newCategory = Category(name=request.form['name'], description=request.form['description'])
			session.add(newCategory)
			session.commit()
			flash("New Category %s Successfully Created!" % newCategory.name)
		else:
			flash("New Category Unsuccessfully Created As Category Name Already Exists")
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
	exist = False
	if request.method == 'POST':
		categorys = session.query(Category).all()
		for c in categorys:
			category_n = c.name
			if request.form['name'] == category_n:
				exist = True
		if exist == False:
			editedCategory.name = request.form['name']
		if request.form['description']:
			editedCategory.description = request.form['description']
		session.add(editedCategory)
		session.commit()
		if exist == False:
			flash("%s Successfully Edited!" % editedCategory.name)
		else:
			flash("%s Unsuccessfully Edited As Category Name Already Exists" % editedCategory.name)
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
		flash("Category %s Successfully Deleted!" % categoryToDelete.name)
		return redirect(url_for('showCatalog'))
	else:
		return render_template('deletecategory.html', category = categoryToDelete)	


#Create new category item
@app.route('/catalog/<category_name>/new/', methods=['GET', 'POST'])
@app.route('/catalog/<category_name>/items/new/', methods=['GET', 'POST'])
def newCategoryItem(category_name):
	category = session.query(Category).filter_by(name=category_name).one()
	category_id = category.id
	exist = False
	if request.method == 'POST':
		items = session.query(CategoryItem).all()
		for i in items:
			item_name = i.name
			if request.form['name'] == item_name:
				exist = True
		if exist == False:
			newItem = CategoryItem(name=request.form['name'], description=request.form['description'],
									  category_id=category_id)
			session.add(newItem)
			session.commit()
			flash("New Item %s Successfully Created" % newItem.name)
		else:
			flash("New Item Unsuccessfully Created As Item Name Already Exists")
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
	exist = False
	if request.method == 'POST':
		items = session.query(CategoryItem).all()
		for i in items:
			item_name = i.name
			if request.form['name'] == item_name:
				exist = True
		if exist == False:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		if exist == False:
			flash("%s Successfully Edited!" % editedItem.name)
		else:
			flash("%s Unsuccessfully Edited As Item Name Already Exists" % editedItem.name)
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
		flash("Item %s Successfully Deleted!" % itemToDelete.name)
		return redirect(url_for('showCategory', category_name=category_name))
	else:
		return render_template('deleteitem.html', category_name=category_name, item_name=item_name, item=itemToDelete)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port = 8000)