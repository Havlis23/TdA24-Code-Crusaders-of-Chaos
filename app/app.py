# app.py

import os
from flask import Flask, render_template
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

teacher_data = {
    "UUID": "67fda282-2bca-41ef-9caf-039cc5c8dd69",
    "title_before": "Mgr.",
    "first_name": "Petra",
    "middle_name": "Swil",
    "last_name": "Plachá",
    "title_after": "MBA",
    "picture_url": "https://tourdeapp.cz/storage/images/2023_02_25/412ff296a291f021bbb6de10e8d0b94863fa89308843b/big.png.webp",
    "location": "Brno",
    "claim": "Aktivní studentka / Předsedkyně spolku / Projektová manažerka",
    "bio": "<p>Baví mě organizovat věci. Ať už to bylo vyvíjení mobilních aplikací ve Futured, pořádání konferencí, spolupráce na soutěžích Prezentiáda, pIšQworky, <b>Tour de App</b> a Středoškolák roku, nebo třeba dobrovolnictví, vždycky jsem skončila u projektového managementu, rozvíjení soft-skills a vzdělávání. U studentských projektů a akcí jsem si vyzkoušela snad všechno od marketingu po logistiku a moc ráda to předám dál. Momentálně studuji Pdf MUNI a FF MUNI v Brně.</p>",
    "tags": [
        {"uuid": "6d348a49-d16f-4524-86ac-132dd829b429", "name": "Dobrovolnictví"},
        {"uuid": "8e0568c3-e235-42aa-9eaa-713a2545ff5b", "name": "Studentské spolky"},
        # ... (other tags)
    ],
    "price_per_hour": 1200,
    "contact": {
        "telephone_numbers": ["+420 722 482 974"],
        "emails": ["placha@scg.cz", "predseda@scg.cz"]
    }
}

@app.route('/')
def hello_world():
    return "Hello TdA"

@app.route('/lecturer')
def teacher_profile():
    return render_template('lecturer.html', teacher_name=f"{teacher_data['first_name']} {teacher_data['last_name']}", teacher_data=teacher_data)

if __name__ == '__main__':
    app.run()
