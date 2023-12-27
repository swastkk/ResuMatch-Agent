import requests
import json

url = "https://indeed12.p.rapidapi.com/job/02eb3a9f080f10e7"

headers = {
	"X-RapidAPI-Key": "6e90ef82cemshd8c60a80c4947ffp15d5fejsnadb81d054fe6",
	"X-RapidAPI-Host": "indeed12.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
jobs= response.json()

for job in jobs.get():
