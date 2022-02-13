# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo

def init_browser():
    # Set up Splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars News URL of page to be scraped
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    news_html = browser.html
    news_soup = bs(news_html, "html.parser")
    # Retrieve the latest news title and paragraph
    news_title = news_soup.find_all("div", class_="content_title")[0].text
    news_paragraph = news_soup.find_all("div", class_="article_teaser_body")[0].text

    # Mars Image to be scraped
    images_url = "https://spaceimages-mars.com/"
    browser.visit(images_url)
    html = browser.html
    images_soup = bs(html, "html.parser")
    # Retrieve featured image link
    image_path = images_soup.find_all('img')[1]["src"]
    featured_image_url = images_url + image_path

    # Mars facts to be scraped, converted into html table
    facts_url = "https://galaxyfacts-mars.com/"
    facts = pd.read_html(facts_url)
    profile = facts[0]
    profile.columns = profile.iloc[0] 
    profile = profile[1:]
    profile.set_index("Mars - Earth Comparison", inplace=True)
    planet_html = profile.to_html()
    planet_html = planet_html.replace("\n", "")
    
    # Mars hemisphere name and image to be scraped
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    # Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    image_info = []
    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find("div", class_="description")
        title = hemisphere.h3.text        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(hemispheres_url + hemisphere_link)        
        image_html = browser.html
        image_soup = bs(image_html, "html.parser")        
        image_link = image_soup.find("div", class_="downloads")
        image_url = "https://marshemispheres.com/" + image_link.find("li").a["href"]
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict["title"] = title
        image_dict["img_url"] = image_url        
        image_info.append(image_dict)

    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_p": news_paragraph,
        "featured_image_url": featured_image_url,
        "fact_table": str(planet_html),
        "hemisphere_images": image_info
    }

    return mars_dict