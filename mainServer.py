from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
#
# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "Restaurant Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# # Create anti-forgery state token
# @app.route('/login')
# def showLogin():
#     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                     for x in xrange(32))
#     login_session['state'] = state
#     # return "The current session state is %s" % login_session['state']
#     return render_template('login.html', STATE=state)
#
#
# @app.route('/gconnect', methods=['POST'])
# def gconnect():
#     # Validate state token
#     if request.args.get('state') != login_session['state']:
#         response = make_response(json.dumps('Invalid state parameter.'), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#     # Obtain authorization code
#     code = request.data
#
#     try:
#         # Upgrade the authorization code into a credentials object
#         oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
#         oauth_flow.redirect_uri = 'postmessage'
#         credentials = oauth_flow.step2_exchange(code)
#     except FlowExchangeError:
#         response = make_response(
#             json.dumps('Failed to upgrade the authorization code.'), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#
#     # Check that the access token is valid.
#     access_token = credentials.access_token
#     url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
#            % access_token)
#     h = httplib2.Http()
#     result = json.loads(h.request(url, 'GET')[1])
#     # If there was an error in the access token info, abort.
#     if result.get('error') is not None:
#         response = make_response(json.dumps(result.get('error')), 500)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#
#     # Verify that the access token is used for the intended user.
#     gplus_id = credentials.id_token['sub']
#     if result['user_id'] != gplus_id:
#         response = make_response(
#             json.dumps("Token's user ID doesn't match given user ID."), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#
#     # Verify that the access token is valid for this app.
#     if result['issued_to'] != CLIENT_ID:
#         response = make_response(
#             json.dumps("Token's client ID does not match app's."), 401)
#         print
#         "Token's client ID does not match app's."
#         response.headers['Content-Type'] = 'application/json'
#         return response
#
#     stored_access_token = login_session.get('access_token')
#     stored_gplus_id = login_session.get('gplus_id')
#     if stored_access_token is not None and gplus_id == stored_gplus_id:
#         response = make_response(json.dumps('Current user is already connected.'),
#                                  200)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#
#     # Store the access token in the session for later use.
#     login_session['access_token'] = credentials.access_token
#     login_session['gplus_id'] = gplus_id
#
#     # Get user info
#     userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
#     params = {'access_token': credentials.access_token, 'alt': 'json'}
#     answer = requests.get(userinfo_url, params=params)
#
#     data = answer.json()
#
#     login_session['username'] = data['name']
#     login_session['picture'] = data['picture']
#     login_session['email'] = data['email']
#
#     output = ''
#     output += '<h1>Welcome, '
#     output += login_session['username']
#     output += '!</h1>'
#     output += '<img src="'
#     output += login_session['picture']
#     output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
#     flash("you are now logged in as %s" % login_session['username'])
#     print
#     "done!"
#     return output
#
#     # DISCONNECT - Revoke a current user's token and reset their login_session
#
#
# @app.route('/gdisconnect')
# def gdisconnect():
#     access_token = login_session['access_token']
#     print
#     'In gdisconnect access token is %s', access_token
#     print
#     'User name is: '
#     print
#     login_session['username']
#     if access_token is None:
#         print
#         'Access Token is None'
#         response = make_response(json.dumps('Current user not connected.'), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#     url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
#     h = httplib2.Http()
#     result = h.request(url, 'GET')[0]
#     print
#     'result is '
#     print
#     result
#     if result['status'] == '200':
#         del login_session['access_token']
#         del login_session['gplus_id']
#         del login_session['username']
#         del login_session['email']
#         del login_session['picture']
#         response = make_response(json.dumps('Successfully disconnected.'), 200)
#         response.headers['Content-Type'] = 'application/json'
#         return response
#     else:
#
#         response = make_response(json.dumps('Failed to revoke token for given user.', 400))
#         response.headers['Content-Type'] = 'application/json'
#         return response


# JSON APIs to view Restaurant Information
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# Show all Categories and Main Page
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html', categories=categories)


# Create a new restaurant


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Edit a restaurant


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Delete a restaurant
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


# Show a restaurant menu


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return render_template('items.html', items=items, category=category)


# Create a new menu item
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'], description=request.form[
            'description'], category_id=category_id)
        session.add(newItem)
        session.commit()
        flash('New Category Item %s Successfully Created' % (newItem.name))
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newcategoryitem.html', category_id=category_id)


# Edit a menu item


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editcategoryitem.html', category_id=category_id, item_id=item_id, item=editedItem)


# Delete a menu item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deletecategoryitem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)