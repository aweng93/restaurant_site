#!/usr/bin/env python

from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem, User
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

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine


# Connect to Database and create database session
def createDBSession():
    session = scoped_session(sessionmaker(bind=engine))
    return session


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    print("server connection")
    if request.args.get('state') != login_session['state']:
        response = make_response(('Invalid state parameter.', 401))
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data.decode("utf-8")
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.0/me"

    url = ("https://graph.facebook.com/v3.0/me?"
           "access_token=%s&fields=name,id,email") % access_token
    print(url)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = access_token

    # Get user picture
    url = ("https://graph.facebook.com/v3.0/me/picture?"
           "access_token=%s&redirect=0&height=200&width=200") % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ " style = "width: 300px;
                    height: 300px;
                    border-radius: 150px;
                    -webkit-border-radius: 150px;
                    -moz-border-radius: 150px;"> """

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ("https://graph.facebook.com/%s"
           "/permissions?access_token=%s") % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session = createDBSession()
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one_or_none()
    session.remove()
    return user.id


def getUserInfo(user_id):
    session = createDBSession()
    user = session.query(User).filter_by(id=user_id).one_or_none()
    session.remove()
    return user


def getUserID(email):
    session = createDBSession()
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        session.remove()
        return user.id
    except ImportError:
        session.remove()
        return None


# JSON APIs to view Information
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    session = createDBSession()
    restaurants = session.query(Restaurant).filter_by(
        id=restaurant_id).one_or_none()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    session.remove()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    session = createDBSession()
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one_or_none()
    session.remove()
    return jsonify(MenuItem=MenuItem.serialize)


@app.route('/restaurant/JSON')
def restaurantsJSON():
    session = createDBSession()
    restaurants = session.query(Restaurant).all()
    session.remove()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# Show all Restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    session = createDBSession()
    restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    session.remove()
    return render_template('restaurants.html', restaurants=restaurants)

# Create a new Restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    session = createDBSession()
    if 'username' not in login_session:
        session.remove()
        return redirect('/login')
    if request.method == 'POST':
        newRestaurant = Restaurant(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newRestaurant)
        flash('New Watch List %s Successfully Created' % newRestaurant.name)
        session.commit()
        session.remove()
        return redirect(url_for('showRestaurants'))
    else:
        session.remove()
        return render_template('newRestaurant.html')


# Edit a Restaurant List
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    session = createDBSession()
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one_or_none()
    if 'username' not in login_session:
        session.remove()
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            session.add(editedRestaurant)
            session.commit()
            flash('Watch List Successfully Edited %s' % editedRestaurant.name)
            session.remove()
            return redirect(url_for('showRestaurants'))
    else:
        session.remove()
        return render_template('editRestaurant.html',
                               restaurant=editedRestaurant)


# Delete a Restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    session = createDBSession()
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one_or_none()
    if 'username' not in login_session:
        session.remove()
        return redirect('/login')
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        session.remove()
        return redirect(url_for('showRestaurants',
                        restaurant_id=restaurant_id))
    else:
        session.remove()
        return render_template('deleteRestaurant.html',
                               restaurant=restaurantToDelete)


# Show a menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    session = createDBSession()
    restaurants = session.query(Restaurant).filter_by(
        id=restaurant_id).one_or_none()
    creator = getUserInfo(restaurants.user_id)
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    session.remove()
    return render_template('menu.html',
                           items=items,
                           restaurant=restaurants,
                           creator=creator)


# Create a new Restaurant item
@app.route('/restaurant/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newItem(restaurant_id):
    session = createDBSession()
    if 'username' not in login_session:
        session.remove()
        return redirect('/login')
    restaurants = session.query(Restaurant).filter_by(
        id=restaurant_id).one_or_none()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           url=request.form['url'],
                           price=request.form['price'],
                           discount=request.form['discount'],
                           category=request.form['category'],
                           in_stock=request.form['in_stock'],
                           restaurant_id=restaurant_id,
                           user_id=restaurants.user_id)
        session.add(newItem)
        session.commit()
        flash('New Item: %s Successfully Created' % (newItem.name))
        session.remove()
        return redirect(url_for('showRestaurants',
                        restaurant_id=restaurant_id))
    else:
        session.remove()
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Edit an item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    session = createDBSession()
    if 'username' not in login_session:
        session.remove()
        return redirect('/login')
    editedItem = session.query(MenuItem).filter_by(
        id=item_id).one_or_none()
    restaurants = session.query(Restaurant).filter_by(
        id=restaurant_id).one_or_none()
    if login_session['user_id'] != restaurants.user_id:
        session.remove()
        return """<script>
                function myFunction() {
                alert('You are not authorized to edit items to this list.');
                }
                </script>
                <body onload='myFunction()'>"""
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['url']:
            editedItem.url = request.form['url']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['discount']:
            editedItem.discount = request.form['discount']
        if request.form['category']:
            editedItem.category = request.form['category']
        if request.form['in_stock']:
            editedItem.in_stock = request.form['in_stock']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        session.remove()
        return redirect(url_for('showRestaurants',
                        restaurant_id=restaurant_id))
    else:
        session.remove()
        return render_template('editMenuItem.html',
                               restaurant_id=restaurant_id,
                               item_id=item_id,
                               item=editedItem)


# Delete an item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    session = createDBSession()
    if 'username' not in login_session:
        session.remove()
        return redirect('/login')
    restaurants = session.query(Restaurant).filter_by(
        id=restaurant_id).one_or_none()
    itemToDelete = session.query(MenuItem).filter_by(id=item_id).one_or_none()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        session.remove()
        return redirect(url_for('showRestaurants',
                        restaurant_id=restaurant_id))
    else:
        session.remove()
        return render_template('deleteMenuItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showRestaurants'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showRestaurants'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='localhost', port=5000, ssl_context=('cert.pem', 'key.pem'))
