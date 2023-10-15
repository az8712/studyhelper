# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as soup
import requests
import re

#Pass in array of keywords as search queries and number of pdfs to scrape
def get_pdfs(queries):
        queries = queries.split(", ")
        url = "https://www.google.com/search?q="
        for q in queries: 
          url += q + "+"
        url += "filetype%3Apdf"

        with requests.Session() as c:
          page_html = c.get(url)
          page_soup = soup(page_html.text, "html.parser")
          containers = page_soup.find_all('div')
          items = []
          for j in containers:
            if "https" in str(j) and "pdf" in str(j):
              if "google" not in str(j):
                #print(re.search("(?P<url>https?://[^\s]+)", str(j)).group("url"))
                temp = str(str(re.search("(?P<url>https?://[^\s]+)", str(j)).group("url")).split('.pdf')[0]) + ".pdf"
                items.append(temp)
          items = list(set(items))
          urls = []
          for i in items:
            if "200" in str(requests.get(i)):
              urls.append(i)
          output = ""
          for i in urls:
            output += i + "<br>"
          return output
#get_pdfs(["Photosynthesis"])


from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("studyhelp2.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    print(text)
    return get_pdfs(text)

app.run(debug=True)

