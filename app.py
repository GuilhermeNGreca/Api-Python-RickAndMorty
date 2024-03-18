from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/RickAndMorty'
CORS(app)

db = SQLAlchemy(app) #permitir a interação com o banco de dados
ma = Marshmallow(app) #fornecer serialização de objetos SQLAlchemy para JSON

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(200))
    species = db.Column(db.String(200))
    type = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(200))
    origin_name = db.Column(db.String(200))
    location_name = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def __init__(self, name, status, species, type, gender, origin_name, location_name, image):
        self.name = name
        self.status = status
        self.species = species
        self.type = type
        self.gender = gender
        self.origin_name = origin_name
        self.location_name = location_name
        self.image = image


class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Character

@app.route('/search', methods=['GET'])
def get_characters():
    page = int(request.args.get('page', 1))
    name_search = request.args.get('name', '')
    status_filter = request.args.get('status', '')

    limit = 20

    query = Character.query.filter(Character.name.ilike(f'%{name_search.lower()}%'))
    if status_filter:
        query = query.filter(Character.status.ilike(status_filter.lower()))

    total_characters = query.count()
    total_pages = (total_characters - 1) // limit + 1
    
    characters = query.limit(limit).offset((page - 1) * limit).all()

    character_schema = CharacterSchema(many=True)
    result = character_schema.dump(characters)

    return jsonify({
        'characters': result,
        'total_pages': total_pages,
        'current_page': page,
        'total_items': min(total_characters, limit)
    })

@app.route('/idsearch', methods=['GET'])
def get_by_id():    
    character_id = request.args.get('id')
    
    character = Character.query.get(character_id)

    character_schema = CharacterSchema()
    result = character_schema.dump(character)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
