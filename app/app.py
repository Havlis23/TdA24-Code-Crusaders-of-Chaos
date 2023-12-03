import os
import uuid
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import MySQLdb

load_dotenv()

connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
)

app = Flask(__name__)


@app.route("/members")
def members():
    return {"members": ["member1", "member2", "member3"]}

@app.route('/')
def hello_world():
    return "Hello TdA"


@app.route("/api/lecturers", methods=["POST", "GET"])
def lecturers():
    if request.method == "POST":
        # Create a new lecturer
        new_lecturer = request.json
        new_lecturer['uuid'] = str(uuid.uuid4())
        new_lecturer['tag_id'] = 1
        new_lecturer['contact_id'] = 1

        with connection.cursor() as cursor:
            sql = """
                INSERT INTO LecturerData (uuid, title_before, first_name, middle_name, last_name, title_after, picture_url, location, claim, bio, tag_id, price_per_hour, contact_id)
                VALUES (%(uuid)s, %(title_before)s, %(first_name)s, %(middle_name)s, %(last_name)s, %(title_after)s, %(picture_url)s, %(location)s, %(claim)s, %(bio)s, %(tag_id)s, %(price_per_hour)s, %(contact_id)s)
                """
            cursor.execute(sql, new_lecturer)
            connection.commit()

        return jsonify(new_lecturer), 200


    elif request.method == "GET":
        # Get all lecturers with tags and contact information from the MySQL database
        with connection.cursor() as cursor:
            sql = """SELECT
                LecturerData.uuid,
                LecturerData.title_before,
                LecturerData.first_name,
                LecturerData.middle_name,
                LecturerData.last_name,
                LecturerData.title_after,
                LecturerData.picture_url,
                LecturerData.location,
                LecturerData.claim,
                LecturerData.bio,
                LecturerData.price_per_hour,
                LecturerTags.name AS tag_name,
                LecturerContact.telephone_number,
                LecturerContact.email
            FROM LecturerData
            LEFT JOIN LecturerTags ON LecturerData.tag_id = LecturerTags.tag_id
            LEFT JOIN LecturerContact ON LecturerData.contact_id = LecturerContact.contact_id
            """
            cursor.execute(sql)
            lecturers_data = cursor.fetchall()

        return jsonify(lecturers_data), 200


@app.route('/api/lecturers/<uuid>', methods=['GET', 'PUT', 'DELETE'])
def lecturer_by_uuid(uuid):
    # Fetch lecturer with tags and contact information from the database based on UUID
    with connection.cursor() as cursor:
        sql = """
        SELECT
        LecturerData.uuid,
        LecturerData.title_before,
        LecturerData.first_name,
        LecturerData.middle_name,
        LecturerData.last_name,
        LecturerData.title_after,
        LecturerData.picture_url,
        LecturerData.location,
        LecturerData.claim,
        LecturerData.bio,
        LecturerData.price_per_hour,
        LecturerTags.name AS tag_name,
        LecturerContact.telephone_number,
        LecturerContact.email
        FROM LecturerData
        LEFT JOIN LecturerTags ON LecturerData.tag_id = LecturerTags.tag_id
        LEFT JOIN LecturerContact ON LecturerData.contact_id = LecturerContact.contact_id
        WHERE LecturerData.uuid = %s
        """
        cursor.execute(sql, (uuid,))
        lecturer_data = cursor.fetchone()

    if lecturer_data is None:
        return jsonify({'code': 404, 'message': 'Lecturer not found'}), 404

    if request.method == 'GET':
        # Extract the relevant data from the lecturer object and organize it into a dictionary
        lecturer_dict = {
            'uuid': lecturer_data[0],
            'title_before': lecturer_data[1],
            'first_name': lecturer_data[2],
            'middle_name': lecturer_data[3],
            'last_name': lecturer_data[4],
            'title_after': lecturer_data[5],
            'picture_url': lecturer_data[6],
            'location': lecturer_data[7],
            'claim': lecturer_data[8],
            'bio': lecturer_data[9],
            'price_per_hour': lecturer_data[10],
            'tags': [{'name': lecturer_data[11]}],  # Assuming 'tag_name' is the 11th column
        }

        # Pass the lecturer dictionary to the template
        return render_template('lecturer.html', lecturer=lecturer_dict)


if __name__ == '__main__':
    app.run(debug=True)
