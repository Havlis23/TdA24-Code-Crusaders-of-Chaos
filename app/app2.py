# app.py

import os
from flask import Flask, jsonify, request, render_template
from . import db

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

# Sample data
teacher_data = {
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

@app.route('/')
def hello_world():
    return "Hello TdA"

@app.route('/api/lecturers', methods=['POST', 'GET'])
def lecturers():
    if request.method == 'POST':
        # Create a new lecturer
        new_lecturer = request.json
        lecturers_data.append(new_lecturer)
        return jsonify(new_lecturer), 200
    elif request.method == 'GET':
        # Get all lecturers
        return jsonify(lecturers_data), 200

@app.route('/api/lecturers/<uuid>', methods=['GET', 'PUT', 'DELETE'])
def lecturer_by_uuid(uuid):
    lecturer = next((item for item in lecturers_data if item["uuid"] == uuid), None)

    if lecturer is None:
        return jsonify({'code': 404, 'message': 'Lecturer not found'}), 404

    if request.method == 'GET':
        # Get a specific lecturer
        return jsonify(lecturer), 200
    elif request.method == 'PUT':
        # Update a specific lecturer
        lecturer.update(request.json)
        return jsonify(lecturer), 200
    elif request.method == 'DELETE':
        # Delete a specific lecturer
        lecturers_data.remove(lecturer)
        return '', 204


@app.route('/teacher')
def teacher_profile():
    return render_template('teacher.html', teacher_name=teacher_data['first_name'], teacher_description=teacher_data['claim'])

if __name__ == '__main__':
    app.run()
