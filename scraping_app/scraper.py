#!/usr/bin/env python

#Initial Setup
from flask import Flask, render_template, request
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

# Create instance of Flask app
app = Flask(__name__)

@app.route("/")
def greeting():
    return "Let's get scraping!  Go to '.../scrape' to begin."

@app.route("/scrape")
# Define scraper function
def scraper():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path,headless=True)

    first_fifty_furn = []
    url = 'https://stlouis.craigslist.org/search/fua?query=mid-century'
    browser.visit(url)

    soup = bs(browser.html,'html.parser')
    furn_divs = soup.find_all('li', class_='result-row')

    for mcm_furn in furn_divs[0:50]:
        try:
            furn_title = mcm_furn.find('a', class_='result-title hdrlnk').text
            furn_date = mcm_furn.find('time', class_='result-date').text
            furn_price = mcm_furn.find('span', class_="result-price").text
            furn_loc = (mcm_furn.find('span', class_="result-hood").text)[2:-2]
            furn_link = mcm_furn.find('a')['href']

            furn_dict = {'Item Name':furn_title,
                        'Date Posted':furn_date,
                        'Price':furn_price,
                        'Seller Location':furn_loc,
                        'Web Link':furn_link
                        }
        
            first_fifty_furn.append(furn_dict)
            
        except AttributeError as e:
            print(e)
    
    first_fifty_furn_df = pd.DataFrame(first_fifty_furn)
    return first_fifty_furn_df
    
    @app.route("scrape/all")
    def display():
        return render_template("index.html", data = x)


if __name__ == "__main__":
    app.run(debug=True)