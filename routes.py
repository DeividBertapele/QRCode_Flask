from flask_dropzone import Dropzone
from flask import Flask, render_template, request, redirect, url_for
from forms import QRCodeData
import secrets
import cv2
import os
import qrcode



app = Flask(__name__)
app.config['SECRET_KEY'] = "JLK24JO3I@!!$#Yoiouoln!#@oo=5y9y9youjuy952ou9859u923kjfhiy23ho"

dir_path = os.path.dirname(os.path.realpath(__file__))


app.config.update(
    UPLOADED_PATH=os.path.join(dir_path, 'static'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1
)
app.config['DROPZONE_REDIRECT_VIEW'] = 'decoded'

dropzone = Dropzone(app)


decoded_info = ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        global decoded_info
        f = request.files.get('file')
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".png"
       
        file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)
        f.save(file_location)

        print(file_location)
        # read and decode QRCode
        img = cv2.imread(file_location)

        det=cv2.QRCodeDetector()

        val, pts, st_code=det.detectAndDecode(img)
        print(val)
        
        os.remove(file_location)
        decoded_info = val
       
    else:
       return render_template("upload.html", title="Home")


@app.route("/generate_qrcode", methods=["GET", "POST"])
def generate_qrcode():
    form =QRCodeData()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data.data
            image_name = f"{secrets.token_hex(10)}.png"
            qrcode_location = f"{app.config['UPLOADED_PATH']}/{image_name}"
            
            try:
                my_qrcode = qrcode.make(str(data))
                my_qrcode.save(qrcode_location)
            except Exception as e:
                print(e)

        return render_template("generated_qrcode.html", title="Generated", image=image_name)

    else:
        return render_template("generate_qrcode.html", title="Generate", form=form)
    
    

if __name__ == "__main__":
    app.run(debug=True)