# Web Scraping Challenge - "Mars Web Application"

This repo highlights the following three data skills:
1. <b>Web scraping</b> a NASA website
2. <b>Storing data</b> with Mongo DB
3. <b>Building a web application</b> through Flask

### 1. Web scraping

Four different website were scraped using the open-source tool <b>[Splinter](https://splinter.readthedocs.io/en/latest/)</b> to automate browser actions...
```python
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
```

and the Python package <b>[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)</b> to parse through HTML...
```python
from bs4 import BeautifulSoup as bs

url = "https://mars.nasa.gov/news/"
browser.visit(url)
html = browser.html
news_site = bs(html, 'html.parser')
```
for scraping relevant data, in this case the latest Mars news headline and first paragraph.
```python
result = news_site.find('div', class_ = 'list_text')
news_title = result.find('a').text
news_para = result.find('div', class_ = 'article_teaser_body').text
```
<br>
This web scraping is assigned as a function [scrape()] in the <em>scrape_mars.py</em> file and is called in the <em>app.py</em> file as a flask route [("/scrape")].

### 2. Storing Data

In the <em>app.py</em> file, I connect to a local <b>[Mongo database](https://www.mongodb.com/resources)</b>...
```python
from flask_pymongo import PyMongo

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
```
then store and update the database with the scraped Mars data - as a route.
```python
@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert = True)
```

### 3. Web Application

Finally, the data is visualized using <b>[Flask](https://flask.palletsprojects.com/en/1.1.x/)</b> to render the html page.
```python
from flask import Flask, render_template, redirect

@app.route("/")
def home():

    data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data = data)
```

### Considerations

I did have trouble displaying the dataframe of Mars facts. After some tinkering, I realized a potential reason is the class attribute of the table.
```python
<table border="1" class="dataframe table">
```
The easiest fix I could think of was changing the HTML script for the table directly in <em>index.html</em>.
```python
<table border="1" class="table">
```
---
### Contact
LinkedIn | https://www.linkedin.com/in/niko-elvambuena/
<br>
Email | niko.elvambuena95@gmail.com
