
import os
import uuid
from flask import Flask, jsonify, request, render_template
from . import db

from dotenv import load_dotenv

load_dotenv()
import os
import MySQLdb

connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY",
    ssl={
        "ca": "/etc/ssl/cert.pem"
    }
)

app = Flask(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)
db.init_app(app)

# Sample data
lecturers_data = [
    {
        'title_before': 'Mgr.',
        'first_name': 'Petra',
        'middle_name': 'Swil',
        'last_name': 'Plachá',
        'title_after': 'MBA',
        'picture_url': 'https://picsum.photos/200',
        'location': 'Brno',
        'claim': 'Bez dobré prezentace je i nejlepší myšlenka k ničemu.',
        'bio': '<b>Formátovaný text</b> s <i>bezpečnými</i> tagy.',
        'tags': [
            {'name': 'Marketing'}
        ],
        'price_per_hour': 720,
        'contact': {
            'telephone_numbers': [
                '+123 777 338 111'
            ],
            'emails': [
                'user@example.com'
            ]
        }
    }
]

@app.route('/')
def hello_world():
    return "Hello TdA"

@app.route("/api/lecturers", methods=["POST", "GET"])
def lecturers():
    if request.method == "POST":
        new_lecturer = request.json if isinstance(request.json, dict) else {}
        new_lecturer['uuid'] = str(uuid.uuid4())[:36]

        # Insert the new lecturer into the PlanetScale database
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO lecturers
            (uuid, title_before, first_name, middle_name, last_name, title_after, picture_url, location, claim, bio, price_per_hour)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    new_lecturer["uuid"],
                    new_lecturer["title_before"],
                    new_lecturer["first_name"],
                    new_lecturer["middle_name"],
                    new_lecturer["last_name"],
                    new_lecturer["title_after"],
                    new_lecturer["picture_url"],
                    new_lecturer["location"],
                    new_lecturer["claim"],
                    new_lecturer["bio"],
                    new_lecturer["price_per_hour"],
                ),
            )

        return jsonify(new_lecturer), 200

    elif request.method == "GET":
        # Get all lecturers from the PlanetScale database
        with connection.cursor() as cursor:
            sql = "SELECT * FROM lecturers"
            cursor.execute(sql)
            lecturers_data = cursor.fetchall()

        return jsonify(lecturers_data), 200

@app.route('/api/lecturers/<uuid>', methods=['GET', 'PUT', 'DELETE'])
def lecturer_by_uuid(uuid):
    # Fetch lecturer from the database based on UUID
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM lecturers WHERE uuid=%s", (uuid,))
        lecturer = cursor.fetchone()

    if lecturer is None:
        return jsonify({'code': 404, 'message': 'Lecturer not found'}), 404

    if request.method == 'GET':
        # Get a specific lecturer
        return render_template('lecturer.html', lecturer=lecturer)

@app.route('/lecturer')
def lecturer_profile():
    return render_template('lecturer.html', teacher_name=f"{lecturers_data['first_name']} {lecturers_data['last_name']}",
                           teacher_data=lecturers_data)

if __name__ == '__main__':
    app.run()
