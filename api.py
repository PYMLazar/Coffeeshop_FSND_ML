import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES

@app.route('/')
def index():
    return jsonify({
        'GET /drinks': 'List drinks (no auth)',
        'GET /drinks-detail': 'List drinks with details (auth required + get:drinks-detail)',
        'POST /drinks': 'Create a drink (auth required + post:drinks)',
        'PATCH /drinks/<id>': 'Update a drink (auth required + patch:drinks',
        'DELETE /drinks/<id>': 'Delete a drink (auth required + delete:drinks)'
    })
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET'])
def list_drinks():
    drinks = list(map(Drink.short, Drink.query.all()))
    print(drinks)
    result = {
        "success": True,
        "drinks": drinks
    }
    return jsonify(result)

#@app.route('/drinks', methods=['GET'])
#def list_drinks(jwt):
 #   return jsonify({'success': True, 'drinks': [d.short() for d in Drink.query.all()]})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def list_drinks_detailed(jwt):
    return jsonify({'success': True, 'drinks': [d.long() for d in Drink.query.all()]})

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

#@app.route('/drinks', methods=['POST'])
#@requires_auth('post:drinks') 
#def create_drink(jwt):
#    title = request.json.get('title', None)
#    recipe = request.json.get('recipe', None)
#
#    byTitle = Drink.query.filter(Drink.title == title).all()
#    if len(byTitle):
#        return abort(422)

#    newDrink = Drink(title=title, recipe=json.dumps(recipe))
#    newDrink.insert()
#    return jsonify({'success': True, 'drinks': [newDrink.long()]})

#Code example provided by Udacity
app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    drink = request.get_json()['drink']
    created_drink = Drink(
    id=drink['id'], title=drink['title'], recipe=drink['recipe'])
    try:
        Drink.insert(created_drink)
    except:
        abort(404)
    return jsonify({"success": True,
                    "drinks": [{"id": drink['id'],
                                "title": drink['title'],
                                "recipe": drink['recipe']}]})

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify(ex.error), ex.status_code
