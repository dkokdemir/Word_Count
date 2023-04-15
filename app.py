import docx
import textract
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from io import BytesIO
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'rtf', 'doc', 'docx', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB file size limit
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension == '.docx':
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    else:
        return textract.process(file_path, encoding='utf-8').decode('utf-8')

def process_text_and_generate_wordcloud(file_path, word_mappings, omit_words, count_numbers=True, language="english"):

    if language == "turkish":
        stemmer = SnowballStemmer("turkish")
        stop_words = set(stopwords.words("turkish"))
    else:
        stemmer = PorterStemmer()
        stop_words = set(stopwords.words("english"))

    text = read_text_from_file(file_path)

    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    if not count_numbers:
        words = [word for word in words if not word.isdigit()]
    words = [word for word in words if word not in stop_words and word not in omit_words]


    for original, replacement in word_mappings.items():
        words = [replacement if word == original else word for word in words]

    word_freq = pd.Series(words).value_counts().to_dict()

    # Generate word cloud
    wordcloud = WordCloud(width=1600, height=900, background_color='white').generate_from_frequencies(word_freq)

    # Save word cloud to a BytesIO object
    img = BytesIO()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(img, format='png')
    img.seek(0)

    return img, word_freq

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Parse word mappings input
            word_mappings_str = request.form.get('word_mappings', '')
            word_mappings = dict([map(str.strip, mapping.split('=')) for mapping in word_mappings_str.split(',') if '=' in mapping])

            # Parse omit words input
            omit_words_str = request.form.get('omit_words', '')
            omit_words = [word.strip() for word in omit_words_str.split(',')]

            # Parse the count_numbers input
            count_numbers = request.form.get('count_numbers') == 'on'

            # Process the text and generate the word cloud
            img, word_freq = process_text_and_generate_wordcloud(file_path, word_mappings, omit_words, count_numbers=count_numbers)


            # Save the word cloud image
            img_filename = f"{str(uuid.uuid4())}_wordcloud.png"
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
            plt.savefig(img_path)

            # Save the word frequencies to a CSV file
            csv_filename = f"{filename}_word_frequencies.csv"
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
            word_freq_df = pd.DataFrame(word_freq.items(), columns=["Word", "Frequency"])
            word_freq_df.to_csv(csv_path, index=False)

            session['img_path'] = img_path
            session['csv_path'] = csv_path
            total_words = word_freq_df.shape[0]

            return render_template('index.html', img_path=img_path, csv_path=csv_path, total_words=total_words)

    return render_template('index.html')

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

#dkokdemir | 02 April 2023 | V 2.0

