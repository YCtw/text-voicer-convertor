from flask import Flask, request, render_template
import gtts
import docx
import shutil
import time


app = Flask(__name__)
# I dont have to do this, as I can directly access my postback file without saving it first.
# UPLOAD_FOLDER = 'C:/Users/yuhan/PycharmProjects/pythonProject/Day90 TTS Convert project/'
# ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


@app.route("/", methods=["GET","POST"])
def home():
    lang = "en"
    if request.method == "POST":
        time.sleep(2)
        language = request.form["language"]
        if language == "English":
            lang = "en"
        elif language == "Chinese":
            lang = "zh-tw"
        content_list = []
        file = request.files['input-file']
        # I don't have to do this, saving file first and use it later since I can use the postback result directly.
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'],'new.docx'))
        doc = docx.Document(file)
        for para in doc.paragraphs:
            content_list.append(para.text)
        recording_string = ''.join(content_list)
        t1 = gtts.gTTS(recording_string, lang=lang)
        t1.save("convert.mp3")
        time.sleep(2)
        shutil.move("convert.mp3", "./static/convert.mp3")
        time.sleep(2)
        return render_template("index.html", done=True)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)