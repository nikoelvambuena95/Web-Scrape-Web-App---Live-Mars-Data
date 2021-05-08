# Web Scraping Challenge - "Mars Web Application"

This repo highlights the following three data skills:
1. **Web scraping** a NASA website
2. **Storing data** with *Mongo DB* 
3. **Building a web application** through *Flask*

### 1. - Web scraping

Four different website were scraped using the Python package *[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)* to parse through HTML...
```python
from bs4 import BeautifulSoup as bs

url = "https://mars.nasa.gov/news/"
response = requests.get(url)
marsSite = bs(response.text, 'html.parser')
```
and scrape for relevant data, in this case the latest Mars news headline and first paragraph.
```python
news_title = marsSite.title.text
news_para = marsSite.body.p.text
```
<br>Using the open-source tool *[Splinter](https://splinter.readthedocs.io/en/latest/)* allowed automated browser actions - i.e. accessing the websites.
```python
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(url)
```
<br>
This web scraping is assigned as a function scrape() in the *scrape_mars.py* file and is called in the *app.py* file as a flask route (/scrape).

### 2. - Storing Data

In the *app.py* file, I connect to a local Mongo database...
```python
from flask_pymongo import PyMongo

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
```
then store and update the database with the scraped Mars data - as a *Flask* route.
```python
@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert = True)
```

### 3. - Web Application

Finally, the data from *Mongo* is visualized in using *Flask* to render an html page.
```python
from flask import Flask, render_template, redirect

@app.route("/")
def home():

    data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data = data)
```

### Considerations

I did have trouble displaying the dataframe of Mars facts. After some tinkering, I realized that one potential reason is the class attribute of the table.
```python
<table border="1" class="dataframe table">
```
The easiest fix I could think of was changing the HTML script for the table directly in *index.html*.
```python
<table border="1" class="table">
```
