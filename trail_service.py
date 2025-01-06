from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import requests
import datetime

# Initialize Flask app and extensions
app = Flask(__name__)
api = Api(app)

# Configure database s
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://MAlmasoudi:WczQ945+@dist-6-505.uopnet.plymouth.ac.uk/COMP2001_MAlmasoudi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Models
class Trail(db.Model):
    __tablename__ = 'Trail'
    trailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trailName = db.Column(db.String(100), nullable=False)
    trailDescription = db.Column(db.String(500))
    trailLength = db.Column(db.Float)   
    trailDifficulty = db.Column(db.String(50), nullable=False)
    trailDateCreated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ownerID = db.Column(db.Integer, nullable=False)

class Location(db.Model):
    __tablename__ = 'Location'
    locationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trailID = db.Column(db.Integer, db.ForeignKey('Trail.trailID'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

# Utility function to authenticate users via Authenticator API
AUTHENTICATOR_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def authenticate_user(email, password):
    response = requests.post(AUTHENTICATOR_URL, json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json()  # Return user data if authenticated
    return None

# RESTful API Resources
class TrailResource(Resource):
    def get(self, trail_id=None):
        if trail_id:
            trail = Trail.query.get(trail_id)
            if not trail:
                return {"message": "Trail not found"}, 404
            return jsonify({
                "trailID": trail.trailID,
                "trailName": trail.trailName,
                "trailDescription": trail.trailDescription,
                "trailLength": trail.trailLength,
                "trailDifficulty": trail.trailDifficulty,
                "trailDateCreated": trail.trailDateCreated,
                "ownerID": trail.ownerID
            })
        else:
            trails = Trail.query.all()
            return jsonify([
                {
                    "trailID": trail.trailID,
                    "trailName": trail.trailName,
                    "trailDescription": trail.trailDescription,
                    "trailLength": trail.trailLength,
                    "trailDifficulty": trail.trailDifficulty,
                    "trailDateCreated": trail.trailDateCreated,
                    "ownerID": trail.ownerID
                } for trail in trails
            ])

    def post(self):
        data = request.get_json()
        # Authenticate user
        user = authenticate_user(data['email'], data['password'])
        if not user:
            return {"message": "Authentication failed"}, 401

        # Create trail
        new_trail = Trail(
            trailName=data['trailName'],
            trailDescription=data.get('trailDescription', ''),
            trailLength=data['trailLength'],
            trailDifficulty=data['trailDifficulty'],
            ownerID=user['userID']
        )
        db.session.add(new_trail)
        db.session.commit()
        return {"message": "Trail created", "trailID": new_trail.trailID}, 201

    def put(self, trail_id):
        trail = Trail.query.get(trail_id)
        if not trail:
            return {"message": "Trail not found"}, 404
        data = request.get_json()
        trail.trailName = data.get('trailName', trail.trailName)
        trail.trailDescription = data.get('trailDescription', trail.trailDescription)
        trail.trailLength = data.get('trailLength', trail.trailLength)
        trail.trailDifficulty = data.get('trailDifficulty', trail.trailDifficulty)
        db.session.commit()
        return {"message": "Trail updated"}, 200

    def delete(self, trail_id):
        trail = Trail.query.get(trail_id)
        if not trail:
            return {"message": "Trail not found"}, 404
        db.session.delete(trail)
        db.session.commit()
        return {"message": "Trail deleted"}, 200

# Register Resources with API
api.add_resource(TrailResource, '/trails', '/trails/<int:trail_id>')

# Main entry point
if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True, host='0.0.0.0')
