from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER=os.path.join(app.root_path,"uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

files=os.listdir(UPLOAD_FOLDER)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )

@app.route('/', methods=['GET', 'POST'])
def home():
    user_ip = request.remote_addr
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    files=os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', ip=user_ip, files=files)

app.run(host='0.0.0.0', port=5000)
