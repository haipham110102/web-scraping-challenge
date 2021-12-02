from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask_pymongo import PyMongo
import pandas as pd
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager



   



def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #1.Nasa News
    url_news = "https://redplanetscience.com/"
    browser.visit(url_news)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #news title and paragraph
    news_title = soup.find('div', class_='content_title').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    #2. JPL mars image
    url_featured = 'https://spaceimages-mars.com/'
    browser.visit(url_featured)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    image_url=soup.find("img", class_="headerimage")
    featured_image_url = url_featured + image_url["src"]


    #3. Mars Facts

    url_fact = 'https://galaxyfacts-mars.com/'
    browser.visit(url_fact)
    table = pd.read_html(url_fact)

    mars_fact=table[1]
    mars_fact.rename(columns={0:"Description", 1:"Value"}, inplace=True)
    html_table = mars_fact.to_html(index = False)
    html_table = html_table.replace("\n", "")
    
    

    #4. hemisphere
    url_hemi = 'https://marshemispheres.com/'
    browser.visit(url_hemi)

    html = browser.html
    soup = bs(html, "html.parser")
    
    results = soup.find_all('div', class_='description')

    hemisphere_image_urls = []
    for result in results:
        title = result.find('h3').text
        hemisphere_url = 'https://marshemispheres.com/' + result.a['href']
    
        browser.visit(hemisphere_url)
        html = browser.html
        soup = bs(html, 'html.parser')
    
    #click on the link to be able to identify wide-image
        img_url = 'https://marshemispheres.com/' + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})



            
    browser.quit()

    mars = {"news_title": news_title, "news_paragraph": news_paragraph, "featured_image_url": featured_image_url, "html_table": html_table, "hemisphere_image_urls": hemisphere_image_urls}

    return mars

