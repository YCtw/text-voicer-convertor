from flask import Flask, request, render_template
import gtts
import docx
import shutil
import time

app = Flask(__name__)

audio_number = 0
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route("/", methods=["GET","POST"])
def home():
    global audio_number
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

        # input is text file
        if file.content_type == "text/plain":
            # since file has been under reviewed above, we need to back the pointer to the beginning
            file.seek(0)
            recording_string = file.read().decode('utf-8')

        #input is docx
        else:
            doc = docx.Document(file)
            for para in doc.paragraphs:
                content_list.append(para.text)
                recording_string = ''.join(content_list)

        #if the converted string is empty
        if recording_string == "":
            return render_template("index.html", is_empty=True)
        else:
            t1 = gtts.gTTS(recording_string, lang=lang)
            audio_number = audio_number + 1
            t1.save(f"{audio_number}convert.mp3")
            time.sleep(2)
            shutil.move(f"{audio_number}convert.mp3", f"./static/{audio_number}convert.mp3")
            time.sleep(2)
            return render_template("index.html", done=True, convert_mp3 = f"./static/{audio_number}convert.mp3")
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
