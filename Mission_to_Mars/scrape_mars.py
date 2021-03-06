# Load dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

################
### NASA Mars News
################
# Splinter set-up
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    news_site = bs(html, 'html.parser')

# Get Latest News Title and Opening Paragraph
    result = news_site.find('div', class_ = 'list_text')
    news_title = result.find('a').text
    news_para = result.find('div', class_ = 'article_teaser_body').text

    browser.quit()
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

# Get Featured Image 'href'
    results = featImg_site.find('div', class_ = 'header')
    featA = results.find('a', class_ = 'showimg fancybox-thumbs')
    featImg_href = featA['href']

# Save complete url string for Featured Image
    partUrl = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    featImg_url = partUrl + featImg_href

    browser.quit()
################
### Mars Facts
################
# Scrape Mars Fact page for facts table
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

# Convert scraped data to Pandas dataframe
    mars_df = tables[0]

# Convert dataframe to HTML table
    mars_htmlTable = (mars_df.to_html(header=False, classes='table'))
    mars_htmlTable = mars_htmlTable.replace('\n', '')

################
### Mars Hemispheres
################
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(url)
    marsHemi = bs(response.text, 'lxml')

# List of results
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

    scrape_data = {
        "news_title" : news_title,
        "news_para" : news_para,
        "featImg_url" : featImg_url,
        "mars_table" : mars_htmlTable,
        "hemisphere_image_urls" : hemisphere_image_urls
    }
    
    browser.quit()

    return scrape_data
