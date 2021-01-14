"""Flask app for Cupcakes"""
from flask import Flask, render_template, flash, redirect, render_template,request,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

def get_cupcake_data(cupcake = None , error_messages = []):
    """Return the Cupcake from request, check and validate data also"""
    print(request.json)

    flavor = request.json.get('flavor' , None)
    size = request.json.get('size' , None)
    rating = request.json.get('rating' , None)
    image = request.json.get('image' , 'https://tinyurl.com/demo-cupcake')

    error_messages = []
    if flavor is None or flavor.strip() == "":
        error_messages.append(('flavor' , 'Flavor is required!'))
    if size is None or size.strip() == "":
        error_messages.append(('size' , 'Size is required!'))
    if rating is None:
        error_messages.append(('rating' , 'Rating is required!'))

    float_rating = 0
    try:
        float_rating = float(rating)
    except:
        error_messages.append(('rating' , 'Rating must be a number'))

    if cupcake is None:
        return Cupcake(flavor=flavor , size=size , rating=rating , image=image)
    
    cupcake.flavor = flavor
    cupcake.size = size
    cupcake.rating = float_rating
    cupcake.image = image

    return cupcake
    
@app.route('/')
def show_index():
    """Show the frontend homepage"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def get_list():
    """Get data about all cupcakes."""

    list = Cupcake.query.all()

    cupcakes = [item.serialize() for item in list]

    return jsonify({"cupcakes" : cupcakes})

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify({"cupcake" : cupcake.serialize()})
@app.route('/api/cupcakes' , methods=['POST'])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request."""
    error_messages = []

    cupcake = get_cupcake_data(error_messages=error_messages)

    if len(error_messages) > 0:
        return jsonify({"error_messages" : error_messages} , 400)
    
    try:
        db.session.add(cupcake)
        db.session.commit()

        return (jsonify({"cupcake" : cupcake.serialize()}) , 201)
    except:
        error_messages.append(('db_error' , 'Error when adding cupcake!'))
        return jsonify({"error_messages" : error_messages} , 400)

@app.route('/api/cupcakes/<int:cupcake_id>' , methods=['PATCH'])
def update_cupdate(cupcake_id):
    """
    Update a cupcake with the id passed in the URL and 
    flavor, size, rating and image data from the body of the request. 
    You can always assume that the entire cupcake object will be passed to the backend.
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    error_messages = []
    cupcake = get_cupcake_data(cupcake=cupcake , error_messages=error_messages)

    print(cupcake)
    print(error_messages)

    if len(error_messages) > 0:
        return jsonify({"error_messages" : error_messages} , 400)
    
    try:
        db.session.commit()
        print(cupcake)
        return jsonify({"cupcake" : cupcake.serialize()})
    except:
        error_messages.append(('db_error' , 'Error when updating cupcake!'))
        # print(error_messages)
        return jsonify({"error_messages" : error_messages} , 400)

@app.route('/api/cupcakes/<int:cupcake_id>' , methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    Cupcake.query.filter_by(id=cupcake_id).delete()

    db.session.commit()

    return jsonify({"message" : "Deleted"})

    




