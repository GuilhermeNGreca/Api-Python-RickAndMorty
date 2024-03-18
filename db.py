import json
import psycopg2

# Conectando ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="RickAndMorty",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Criação da tabela Character
cur.execute("""
    CREATE TABLE IF NOT EXISTS Character (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        status VARCHAR(200),
        species VARCHAR(200),
        type VARCHAR(200),
        gender VARCHAR(200),
        origin_name VARCHAR(200),
        location_name VARCHAR(200),
        image VARCHAR(200)
    );
""")
conn.commit()

# Populando a tabela com dados do arquivo JSON
with open('C:\\Users\\User\\Desktop\\Characters.json', encoding='utf-8-sig') as file:
    characters_data = json.load(file)

    sorted_characters = sorted(characters_data, key=lambda x: x["id"])

    for character in sorted_characters:
        name = character['name']
        status = character['status']
        species = character['species']
        type_ = character.get('type')
        gender = character['gender']
        origin_name = character['origin']['name']
        location_name = character['location']['name']
        image = character['image']

        cur.execute("""
            INSERT INTO Character (name, status, species, type, gender, origin_name, location_name, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (name, status, species, type_, gender, origin_name, location_name, image))

conn.commit()
conn.close()

print('Database populated successfully.')
