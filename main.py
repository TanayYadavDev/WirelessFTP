from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        file = request.files['file']

        if file.filename != '':
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    return render_template('index.html')

app.run(host='0.0.0.0', port=5000)
