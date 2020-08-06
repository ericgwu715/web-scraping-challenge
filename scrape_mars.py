from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_everything():
    browser = init_browser()
    mars_data = {}

    ##### Headlines #####
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    news = soup.find_all('div', class_='list_text')
    mars = []
    for news_item in news:
        news_title = news_item.find('div', class_='content_title').text
        news_paragraph = news_item.find('div', class_='article_teaser_body').text
        mars.append({'title' : news_title, 'paragraph' : news_paragraph})

    # Update mars_data
    mars_data['headline'] = mars_news[0]['title']
    mars_data['headline_paragraph'] = mars_news[0]['paragraph']

    ##### Featured Image #####
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    base_url = 'https://www.jpl.nasa.gov'
    full_image_button = soup.find('a', id='full_image')
    full_href = full_image_button.get('data-fancybox-href')
    featured_image_url = base_url + full_href

    # Update mars_data
    mars_data['featured_image_url'] = featured_image_url

    ##### Weather #####
    twitter_mars_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_mars_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('p', class_='TweetTextSize').text

    # Update mars_data
    mars_data['current_weather'] = mars_weather

    ##### Facts #####
    mars_facts = 'https://space-facts.com/mars/'
    response = requests.get(mars_facts_url)
    html = response.content
    df = pd.read_html(html)
    df_html = df[0].to_html()

    # Update mars_data
    mars_data['facts'] = df_html

    #### Mars Hemispheres ####
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)
    time.sleep(2)
    links = browser.find_by_css('.description .itemLink')
    hemisphere_image= []
    hrefs = []
    titles = []
    for link in links:
        hrefs.append(link['href'])
        titles.append(link.text)

    current_index = 0
    for href in hrefs:
        browser.visit(href)
        time.sleep(1)
        css_image = '.downloads ul li a'
        image_link = browser.find_by_css(css_image)[0]
        hemisphere_image.append({"title" : titles[current_index], "img_url" : image_link['href']})
        current_index += 1

    # Update mars_data
    mars_data['hemispheres'] = hemisphere_image

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data