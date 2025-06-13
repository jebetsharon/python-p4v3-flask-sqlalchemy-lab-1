# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    # __define-ocg__
    eq = Earthquake.query.get(id)
    if eq is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    return jsonify({
        "id":        eq.id,
        "location":  eq.location,
        "magnitude": eq.magnitude,
        "year":      eq.year
    }), 200

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_quakes_by_magnitude(magnitude):
    results = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes = [{
        "id":        e.id,
        "location":  e.location,
        "magnitude": e.magnitude,
        "year":      e.year
    } for e in results]
    return jsonify({
        "count": len(quakes),
        "quakes": quakes
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
