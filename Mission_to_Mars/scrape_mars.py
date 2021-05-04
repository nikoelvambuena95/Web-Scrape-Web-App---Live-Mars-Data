from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

################
### NASA Mars News
################
# Load dependencies

url = "https://mars.nasa.gov/news/"
response = requests.get(url)

# Create a BS object
marsSite = bs(response.text, 'html.parser')

print(marsSite.prettify())

# Create News Title and Paragraph variables 
newsTitle = marsSite.title.text
newsPara = marsSite.body.p.text
print(newsTitle)
print(newsPara)
################
### JPL Mars Space Images - Featured Image
################
# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(url)

# HTML object
html = browser.html
featImg_site = bs(html, 'html.parser')
print(featImg_site.prettify())

# url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
# browser.visit(url)

# Get Featured Image 'href'
results = featImg_site.find('div', class_ = 'header')
featA = results.find('a', class_ = 'showimg fancybox-thumbs')
featImg_href = featA['href']

# Save complete url string for Featured Image
partUrl = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
featured_image_url = partUrl + featImg_href
featured_image_url

browser.quit()
################
### Mars Facts
################
# Scrape Mars Fact page for facts table
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
tables

# Convert scraped data to Pandas dataframe
mars_df = tables[0]

# Convert dataframe to HTML table
mars_htmlTable = mars_df.to_html()
mars_htmlTable
################
### Mars Hemispheres
################
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
response = requests.get(url)
marsHemi = bs(response.text, 'lxml')
print(marsHemi.prettify())

# List of results
# results = marsHemi.find_all('div', class_ = "item")
results = marsHemi.find_all('a', class_ = "itemLink product-item")

# Loop through returned results
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://astrogeology.usgs.gov"
hemisphere_image_urls = []

for result in results:
    dict = {}
    href = result['href']
    imgSite = url + href
    browser.visit(imgSite)
    html = browser.html
    featImg_site = bs(html, 'lxml')
    # Identify full-resolution image container
    title = featImg_site.title.text.strip()
    title = title.replace(" Enhanced | USGS Astrogeology Science Center", "")
    images = featImg_site.find('li')
    img_url = images.find('a')['href']
    dict['title'] = title
    dict['img_url'] = img_url
    hemisphere_image_urls.append(dict)
    
browser.quit()
print(hemisphere_image_urls)