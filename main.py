import io
import operator
import re

import docx2txt
import matplotlib.pyplot as plt
from flask import Flask, render_template_string, request
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud

# Docx resume
# Wordcloud
set(stopwords.words("english"))
app = Flask(__name__)


def read_pdf_resume(pdf_doc):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_doc, "rb") as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text


def read_word_resume(word_doc):
    resume = docx2txt.process(word_doc)
    resume = str(resume)
    # print(resume)
    text = "".join(resume)
    text = text.replace("\n", "")
    if text:
        return text


def clean_job_decsription(jd):
    """a function to create a word cloud based on the input text parameter"""
    ## Clean the Text
    # Lower
    clean_jd = jd.lower()
    # remove punctuation
    clean_jd = re.sub(r"[^\w\s]", "", clean_jd)
    # remove trailing spaces
    clean_jd = clean_jd.strip()
    # remove numbers
    clean_jd = re.sub("[0-9]+", "", clean_jd)
    # tokenize
    clean_jd = word_tokenize(clean_jd)
    # remove stop words
    stop = stopwords.words("english")
    clean_jd = [w for w in clean_jd if not w in stop]
    return clean_jd


def create_word_cloud(jd):
    corpus = jd
    FreqDist(corpus)
    # print(fdist.most_common(100))
    words = " ".join(corpus)
    words = words.split()

    # create a empty dictionary
    data = dict()
    #  Get frequency for each words where word is the key and the count is the value
    for word in words:
        word = word.lower()
        data[word] = data.get(word, 0) + 1
    # Sort the dictionary in reverse order to print first the most used terms
    dict(sorted(data.items(), key=operator.itemgetter(1), reverse=True))
    word_cloud = WordCloud(
        width=800, height=800, background_color="white", max_words=500
    )
    word_cloud.generate_from_frequencies(data)
    plt.figure(figsize=(10, 8), edgecolor="k")
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    # plt.show()


def get_resume_score(text):
    cv = CountVectorizer(stop_words="english")
    count_matrix = cv.fit_transform(text)
    # Print the similarity scores
    print("\nSimilarity Scores:")

    # get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2)  # round to two decimal
    return matchPercentage

    # print(
    #     "Your resume matches about "
    #     + str(matchPercentage)
    #     + "% of the job description."
    # )


HTML_TEMPLATE = """
<!doctype html>
<title>Upload File and Text Input</title>
<h1>Upload File and Add Text</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=text name=textinput>
  <input type=submit value=Upload>
</form>
"""


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        text_input = request.form["textinput"]
        filename = file.filename
        file.save(filename)
        resume = read_pdf_resume(f"./{filename}")
        clean_jd = clean_job_decsription(text_input)
        create_word_cloud(clean_jd)
        text = [resume, text_input]
        score = get_resume_score(text)
        if text_input:
            return f"matched about : {score}%"
    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True)
