
# Dependencies
import pandas as pd
import datetime as dt

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
#_____________________


### Initiate Browser and scrape all data #######################
def scrape_all():
	# Path
	executable_path = {'executable_path':ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=True)

	news_title, news_paragraph = mars_news(browser)

	data = {"news_title": news_title,
			"news_paragraph": news_paragraph,
			"featured_image": featured_image(browser),
			"facts": mars_facts(),
			"last_modified": dt.datetime.now(),
			"hemispheres": hemispheres(browser)}

	browser.quit()
	return data



### MISSION TO MARS - ARTICLES ##############################

# Scrape mars news
def mars_news(browser):
	
	# Visit site
	url = 'https://redplanetscience.com'
	browser.visit(url)

	# Optional delay
	browser.is_element_present_by_css('div.list_text', wait_time=1)

	# Parse html
	html = browser.html
	news_soup = soup(html, 'html.parser')

	try:
		# Parent Element
		slide_elem = news_soup.select_one('div.list_text')  
		# Scrape title
		news_title = slide_elem.find('div',  class_='content_title').get_text()
		# Scrape article summary
		news_p = slide_elem.find('div',  class_='article_teaser_body').get_text()
	except AttributeError:
		return None, None	

	return news_title, news_p


### JPL's SPACEIMAGES - IMAGES ###############################

# Scrape Featured Image
def featured_image(browser):
	# Visit website
	url = 'https://spaceimages-mars.com'
	browser.visit(url)

	# Find and click full image button
	full_image_elem = browser.find_by_tag('button')[1]
	full_image_elem.click()

	# Parse using Soup
	html = browser.html
	img_soup = soup(html, 'html.parser')

	try:
		# Find the relative image url
		img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
	except AttributeError:
		return None

	# Build full url
	img_url = f'https://spaceimages-mars.com/{img_url_rel}'

	return img_url


### MARS FACTS - #######################################

# Scrape Mars Facts:
def mars_facts():
	try:
		# Read table data from Mars Facts
		mars_df = pd.read_html('https://galaxyfacts-mars.com')[0]
	except BaseException:
		return None

	mars_df.columns=['description', 'Mars', 'Earth']
	mars_df.set_index('description', inplace=True)

	return mars_df.to_html()


def hemispheres(browser):
	# Visit website
	url = 'https://marshemispheres.com/'
	browser.visit(url)

	hemisphere_image_urls = []

	# Parse the html
	hemi_html = browser.html
	hemi_soup = soup(hemi_html, 'html.parser')
	# Find all image/hemisphere items
	all_img = hemi_soup.find_all("div", class_="description")

	# Loop through each hemisphere item to get to final high res image
	try:
		for item in all_img:
		    hemispheres = {}    
		    hemisphere_link = item.find("a").get("href")
		    title = item.find("h3").get_text()
		    hemispheres["title"]=title

		    visit_hemi = url+hemisphere_link
		    browser.visit(visit_hemi)
		    
		    each_hemi_html = browser.html
		    each_hemi_soup = soup(each_hemi_html,'html.parser')
		    each_hemi_url = each_hemi_soup.find('img', class_='wide-image').get('src')
		    final_img_url=url+each_hemi_url
		    hemispheres["img_url"]=final_img_url
		    
		    hemisphere_image_urls.append(hemispheres)
		    browser.back()
	except AttributeError:
		return None

	return hemisphere_image_urls



if __name__ == "__main__":
	# If running as script, print scraped data
	print(scrape_all())

