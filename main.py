from flask import Flask, render_template, request, send_from_directory
import qrcode, socket
import os

app = Flask(__name__)

UPLOAD_FOLDER=os.path.join(app.root_path,"uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

STATIC_FOLDER=os.path.join(app.root_path,"static")
os.makedirs(STATIC_FOLDER,exist_ok=True)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )

@app.route('/', methods=['GET', 'POST'])
def home():    
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    files=os.listdir(UPLOAD_FOLDER)
    
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    server_ip=s.getsockname()[0]
    s.close()
    
    qr=qrcode.make("http://"+server_ip+":5000")
    qr.save(
        os.path.join(
            STATIC_FOLDER,
            "qrcode.png"
        )
    )
    return render_template('index.html', files=files)

    
app.run(host='0.0.0.0', port=5000)
