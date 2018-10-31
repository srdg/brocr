import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image

if not os.path.exists(os.getcwd()+'/uploads'):
    os.makedirs( os.getcwd()+'/uploads')
UPLOAD_FOLDER = os.getcwd()+'/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
lang = ''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global lang
    if request.method == 'POST':

        lang = request.form["lang"]
        #print(lang,type(lang))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("index.html")


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    global lang
    # perform ocr at this point
    ocr_text=pytesseract.image_to_string(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)),lang=lang)
    # remove uploaded file to eliminate redundancies and use less storage
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("ocr.html",content=ocr_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)