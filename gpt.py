import os

import requests
from dotenv import load_dotenv
from pyresparser import ResumeParser

load_dotenv()

API_KEY = os.getenv("OPEN_API_KEY")
# Replace with your actual API endpoint and key
chatgpt_api_endpoint = (
    "https://api.openai.com/v1/engines/chatgpt-model-name/completions"
)
headers = {"Authorization": f"{API_KEY}"}


def parse_resume(resume_path):
    # Parse the resume
    data = ResumeParser(resume_path).get_extracted_data()
    return data


def score_resume(resume_data, job_description):
    # Format the data for the ChatGPT API
    prompt = f"Please evaluate the following resume based on the job description provided: \nResume: {resume_data}\nJob Description: {job_description}\nScore:"

    response = requests.post(
        chatgpt_api_endpoint,
        headers=headers,
        json={"prompt": prompt, "max_tokens": 150},
    )
    if response.status_code == 200:
        return response.json().get("choices")[0].get("text").strip()
    else:
        return "Error in ChatGPT API response"


# Path to your resume file
resume_path = "path/to/resume.pdf"
# Example job description
job_description = "Job description data here"

# Parse the resume
resume_data = parse_resume(resume_path)

# Score the resume
resume_score = score_resume(resume_data, job_description)
print("Resume Score:", resume_score)
