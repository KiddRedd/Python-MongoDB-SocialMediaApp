from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# MongoDB configuration # Use the one you need
client = MongoClient('mongodb+srv://<username>:<password>@mongodbxadasd/admin?replicaSet=replicaset&tls=true')
#client = MongoClient ('mongodb://localhost:27017')

db = client['users_db']
collection = db['users']

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    location = request.form.get('location')
    profession = request.form.get('profession')
    
    # Save the profile picture
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join('/path/to/save/pictures', filename))
            collection.insert_one({
                "first_name": first_name,
                "last_name": last_name,
                "location": location,
                "profession": profession,
                "profile_picture": filename
            })
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
