import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time

#dictionary with all data
mars_data={}

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True, user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')


url_1 = 'https://mars.nasa.gov/news/'


browser.visit(url_1)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

search = soup.find('section', class_= 'grid_gallery module list_view')


title_search = search.find_all('div', class_= 'content_title',limit=1)
p_search = search.find_all('div', class_='article_teaser_body',limit=1)


news_title = title_search[0].a.text
news_p = p_search[0].text

#add data to dictionary
mars_data['news_title']=news_title
mars_data['news_p']=news_p


url_2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'



browser.visit(url_2)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')



#click the full image button
click1=browser.links.find_by_partial_text('FULL IMAGE').click()


#click the more info button
click2=browser.links.find_by_partial_text('more info').click()

#parse the page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


#find the link to the full size image
img_partial = soup.find_all('img',class_='main_image')[0]['src']


featured_img_url = f'https://www.jpl.nasa.gov{img_partial}'

mars_data['featured_img_url']=featured_img_url
featured_img_url


twitter_url = 'https://twitter.com/MarsWxReport?lang=en'


browser.visit(twitter_url)
time.sleep(2)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


tweet_search = soup.find_all('article')
mars_weather=tweet_search[0].find_all('span')[4].text

mars_data['mars_weather']=mars_weather
mars_weather


facts_url = 'https://space-facts.com/mars/'

browser.visit(facts_url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


facts_table = pd.read_html(facts_url)

mars_table = facts_table[0]


mars_table = mars_table.rename(columns = {0:'Mars Planet Profile',1:''})

mars_table = mars_table.set_index('Mars Planet Profile', drop=True)

mars_table

mars_table.to_html('mars_html')

mars_data['mars_facts']=mars_table.to_html(justify='left')

hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
base_url = 'https://astrogeology.usgs.gov/'

browser.visit(hemisphere_url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#click the image link to get to the page with the full res image
browser.find_by_css('img[class="thumb"]')[0].click()

#get html again after clicking page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#find image link and title
img_search = soup.find_all('img',class_='wide-image' )
title_search = soup.find_all('h2',class_='title')

#titles had the word 'enhanced' at the end, just getting rid of that
' '.join(title_search[0].text.split(' ')[:-1])

img_link = base_url + img_search[0]['src']

img_link

#do all of the step above for each hemisphere
img_urls =[]
titles=[]
for i in range(4):
    browser.visit(hemisphere_url)
    time.sleep(1)
    browser.find_by_css('img[class="thumb"]')[i].click()
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_search = soup.find_all('img',class_='wide-image' )
    title_search = soup.find_all('h2',class_='title')
    titles.append(' '.join(title_search[0].text.split(' ')[:-1]))
    img_urls.append(base_url + img_search[0]['src'])

img_urls

titles

hemisphere_image_urls = []
urls ={}
for i in range(4):
    urls['title']=titles[i]
    urls['img_url']=img_urls[i]
    hemisphere_image_urls.append(urls)
    urls={}

mars_data['hemisphere_image_urls']=hemisphere_image_urls
hemisphere_image_urls


print('scraped')
print(mars_data)