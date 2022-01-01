#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#Create a function called scrape_all that calls the other functions
def scrape_all():
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    hemispheres=hemisphere_data(browser)

    #Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "hemispheres":hemispheres,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    #Stop webdriver and return data
    browser.quit()
    return data

#Create a function called mars_news
def mars_news(browser):

    #Visit the Quotes to Scrape site
    url= 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Setup the html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add a try/except in case there's an issue
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

#Create a function to scrape hemisphere data
def hemisphere_data(browser):

    #Visit the Mars Hemisphere url to Scrape site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create empty list of dictionaries
    hemisphere_image_urls = []

    #Setup the html parser
    html = browser.html
    hem_soup = soup(html, 'html.parser')

    #Add a try/except in case there's an issue
    try:
        #search for all div elements with class item
        hem_div = hem_soup.find_all('div', class_='item')
        
        #for each item in hem_div, find all h3 tag elements
        #use the h3 text to click the corresponding link
        #once in the next page, find all a tags
        #if the a tag's string equals Sample, 
        #then capture it's associated href
        for links in hem_div:
            link_title=links.find('h3').text
            browser.links.find_by_partial_text(link_title).click()
            page2html = browser.html
            page2_soup=soup(page2html, 'html.parser')
            full_img_links=page2_soup.find_all('a')
            for hrefs in full_img_links:
                if hrefs.string=='Sample':
                    img_url_rel=hrefs.get('href')
                    img_url=f'{url}{img_url_rel}'
            hemisphere_image_urls.append({"img_url":img_url, "title": link_title}) 
            
            browser.back()

    except AttributeError:
        return None

    return hemisphere_image_urls

#Create a function to get featured image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    #Create the full path / url to the image
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        #Read the table from the galaxyfacts-mars website
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)


    #Convert the dataframe to html
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    #If running as script, print scraped data
    print(scrape_all())

