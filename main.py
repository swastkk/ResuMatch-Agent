import io

import docx2txt
from flask import Flask, render_template_string, request
from nltk.corpus import stopwords
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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


def get_resume_score(text):
    cv = CountVectorizer(stop_words="english")
    count_matrix = cv.fit_transform(text)
    # Print the similarity scores
    print("\nSimilarity Scores:")

    # get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2)  # round to two decimal
    return matchPercentage


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
        text = [resume, text_input]
        score = get_resume_score(text)
        if text_input:
            return f"matched about : {score}%"
    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True)
