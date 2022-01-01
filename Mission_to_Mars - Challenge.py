#!/usr/bin/env python
# coding: utf-8

# In[169]:


#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[170]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[171]:


#Visit the Quotes to Scrape site
url= 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[172]:


#Setup the html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[173]:


slide_elem.find('div', class_='content_title')


# In[174]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[175]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images
# 

# In[176]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[177]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[178]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[179]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[180]:


#Create the full path / url to the image
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[181]:


#Read the table from the galaxyfacts-mars website
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[182]:


#Convert the dataframe to html
df.to_html()


# In[183]:


### D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles ###


# In[184]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[185]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hem_soup = soup(html, 'html.parser')
hem_div = hem_soup.find_all('div', class_='item')


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
            #print(img_url)
    hemisphere_image_urls.append({"img_url":img_url, "title": link_title}) 
    
    browser.back()
    #print(full_img_links)


# In[186]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[187]:


# 5. Quit the browser
browser.quit()


# In[ ]:




