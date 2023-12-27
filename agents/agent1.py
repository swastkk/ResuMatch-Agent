import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from uagents import Agent, Context, Model

from .job_desc import job_desc


class Message(Model):
    message: str


def get_resume_score(text):
    cv = CountVectorizer(stop_words="english")
    count_matrix = cv.fit_transform(text)
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    print(matchPercentage)
    matchPercentage = round(matchPercentage, 2)  # round to two decimal
    return matchPercentage


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


agent1 = Agent(
    name="agent1",
    port=8001,
    seed="agent1 secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)


@agent1.on_event("startup")
async def start(ctx: Context):
    resume = input("enter file \n")
    jd = job_desc
    resume_text = read_pdf_resume(resume)
    score = get_resume_score([resume_text, jd])

    if score >= 50:
        await ctx.send(
            "agent1qdp9j2ev86k3h5acaayjm8tpx36zv4mjxn05pa2kwesspstzj697xy5vk2a",
            Message(
                message=f"Accepted with score above 50% \n. Your score is {score} %"
            ),
        )
    else:
        await ctx.send(
            "agent1qdp9j2ev86k3h5acaayjm8tpx36zv4mjxn05pa2kwesspstzj697xy5vk2a",
            Message(
                message=f"Rejected with score below 50% \n. Your score is {score} %"
            ),
        )


if __name__ == "__main__":
    agent1.run()
