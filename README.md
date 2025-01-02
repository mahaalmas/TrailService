# TrailService
This service is a core component of the Trail Application, enabling seamless data management and secure access.
# Introduction
The TrailService micro-service manages trail-related information, including trail details, waypoints, and user authentication. It provides CRUD operations and integrates with an Authenticator API for secure user validation. This service is a core component of the Trail Application, enabling seamless data management and secure access.
This paper contains a full overview of the TrailService microservice, such as its reason, architecture, main features and tech stack. Specific sections include the address of the API endpoints, database schema, geospatial features and integration patterns with other microservices. Besides, some instructions for the service deployment are also incorporated using containerized and orchestration. For continued investigation, service source code is available in its GitHub repository, and live service implementation in its hosted microservice is provided.
# Database Design
The database design supports the key entities for managing trail and location data. The following tables were created:
Trail: Stores trail details, such as name, description, length, difficulty, and ownership.
Location: Holds latitude and longitude for trail waypoints and links to the Trail table via a foreign key.
The Entity Relationship Diagram (ERD) illustrates the relationships between these tables. The Trail table is the primary entity, with a one-to-many relationship with the Location table, representing waypoints.

# Micro-Service Design
The TrailService micro-service provides a RESTful API for managing trail and location data. Below are the main design components:
API Endpoints:
Method
# Endpoint
Description
GET
/trails
Fetch all trails.
GET
/trails/int:trail_id
Fetch details of a specific trail.
POST
/trails
Create a new trail.
PUT
/trails/int:trail_id
Update an existing trail.
DELETE
/trails/int:trail_id
Delete a trail.

# Legal, Social, Ethical, and Professional (LSEP) Considerations
  # Legal:
Minimal data collection and anonymization (e.g., hashed passwords).
Role-based access control to protect sensitive operations.

  # Social:
JSON-based data ensures accessibility.
Promotes outdoor activities for improved well-being.

  # Ethical:
Transparent and fair data handling.
Data used solely for trail management.

  # Professional:
Secure and consistent operations with audit logs and backups.

# Implementation
The micro-service was implemented using Flask and integrates with Microsoft SQL Server through SQLAlchemy. Below are the key components:
Database Configuration:

 app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://username:password@dist-6-505.uopnet.plymouth.ac.uk/TrailDB'
db = SQLAlchemy(app)


# Trail Model:

 # class Trail(db.Model):
    __tablename__ = 'Trail'
    trailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trailName = db.Column(db.String(100), nullable=False)
    trailDescription = db.Column(db.String(500))
    trailLength = db.Column(db.Float)
    trailDifficulty = db.Column(db.String(50), nullable=False)
    trailDateCreated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ownerID = db.Column(db.Integer, nullable=False)


# Location Model:

 # class Location(db.Model):
    __tablename__ = 'Location'
    locationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trailID = db.Column(db.Integer, db.ForeignKey('Trail.trailID'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


# User Authentication: The Authenticator API was integrated to validate user credentials before allowing trail creation or modification.

 def authenticate_user(email, password):
    response = requests.post(AUTHENTICATOR_URL, json={"email": email, "password": password})
    return response.json() if response.status_code == 200 else None
# Testing and Evaluation
Testing verified the functionality, security, and performance of the micro-service.

# Functional Testing:


CRUD operations were tested using Postman.
# Example Input for Trail Creation:
 {
    "email": "user@example.com",
    "password": "securepassword",
    "trailName": "Mountain Trail",
    "trailDescription": "Scenic mountain trail.",
    "trailLength": 8.5,
    "trailDifficulty": "Moderate"
}


Expected Output: HTTP 201 with trail ID.
# Security Testing:
Authentication validated via the Authenticator API.
SQL injection prevented through parameterized queries.

# Areas for Improvement:
Add token-based authentication (e.g., JWT) for enhanced security.
Implement detailed error handling for edge cases.

# Summary
The TrailService micro-service is a secure, RESTful application that efficiently manages trail data and integrates with an external authentication service. While robust in its current implementation, future improvements could include token-based authentication and enhanced error handling for a better user experience.





