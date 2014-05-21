from bs4 import BeautifulSoup as BS
from datetime import datetime
import urllib, urllib2
import os
import csv
import json

def static_url(url):
	static_url = "www.dealmoon.com"
	if static_url in url:
		return url
	else:
		return static_url + url

def image_src(img):
	img_src = ""
	if img.has_attr('src'):
		img_src = img['src']
	if img.has_attr('data-original'):
		img_src = img['data-original']
	if "dealmoon.com" in img_src:
		return img_src
	else:
		return static_url_en + img_src

def escape_special_chars(str):
	return str.replace('/', '|')

url = "http://www.dealmoon.com/Hot-Picks/"
static_url_en = "http://www.dealmoon.com"
html = urllib2.urlopen(url)
soup = BS(html)

folder_name = str(datetime.now()).split(' ')[0]
path = folder_name + "/img/"
if not os.path.exists(path):
	os.makedirs(path)
json_data = {}

# get the whole deal div
div_ml = soup.find('div', 'ml')
# get the subtitle
subtitle = div_ml.find('div', 'sub_rititle').find('h2').get_text()
json_data['subtitle'] = subtitle
# get the page link number & the first five links
cur_page = div_ml.find('div', 'pagelink').find('span', 'current_link').get_text()
first_five_links = div_ml.find('div', 'pagelink').find_all('a', 'link')

#get data from the first page
div_mlist = soup.find_all('div', 'mlist')
div_list_len = len(div_mlist)
json_data['length'] = div_list_len
deals_list = []
for single_deal in div_mlist:
	single_deal_data = {}
	# get the data-id
	data_id = single_deal['data-id']
	single_deal_data['id'] = data_id
	# get the category & time
	deal_category = single_deal.find('div', 'more').find('a').get('href').encode('utf-8')
	deal_created_time = single_deal.find('div', 'date2').get_text().replace('ago', '').strip()
	single_deal_data['category'] = deal_category
	# print data_id
	# get the image
	img_wrap = single_deal.find('div', 'img_wrap')
	image = img_wrap.find('img')
	img_title = image['title']
	img_src = image_src(image)
	# single_deal_data['image_url'] = img_src
	img_format = img_src.split(".")[-1]
	# 1st way to get image saved locally
	"""
	output = open(img_title + '.' + img_format, 'wb')
	output.write(urllib2.urlopen(img_src).read())
	output.close()
	"""
	#	2nd way to get image saved locally
	urllib.urlretrieve(img_src, path + data_id + '_' + escape_special_chars(img_title) + '.' + img_format)
	
	# get the deal name
	div_mtxt_header = single_deal.find('div', 'mtxt').find('h2').find('a')
	div_mtxt_link = div_mtxt_header.get('href').encode('utf-8')
	div_mtxt_name = (div_mtxt_header.find_all('span')[0].get_text().strip() + ' ' + div_mtxt_header.find_all('span')[1].get_text().strip()).encode('utf-8')
	single_deal_data['name'] = div_mtxt_name
	single_deal_data['link'] = div_mtxt_link

	# get the deal detail
	div_mbody_uls = single_deal.find('div', 'mbody').find_all('ul')
	ul_list_len = len(div_mbody_uls)
	if (ul_list_len >= 1):
		deal_detail = div_mbody_uls[0].get_text().strip()
		single_deal_data['description'] = deal_detail
		ul_a_len = len(div_mbody_uls[0].find_all('a'))
		if (ul_a_len > 0):
			deal_official_link = div_mbody_uls[0].find_all('a')[0].get('href')
			deal_official_name = div_mbody_uls[0].find_all('a')[0].get_text()
			single_deal_data['official_weblink'] = static_url(deal_official_link)
		if (ul_list_len == 2):
			dealmoon_recommends = div_mbody_uls[1].find_all('a')
			recommends = []
			for recommend in dealmoon_recommends:
				deal_recommend = {}
				deal_recommend['name'] = recommend.get_text()
				deal_recommend['link'] = recommend.get('href')
				recommends.append(deal_recommend)
			single_deal_data['recommends'] = recommends
		if (ul_list_len >= 3):
			other_descriptions = []
			for i in range(1, ul_list_len):
				other_descriptions.append(div_mbody_uls[i].get_text())
			single_deal_data['other_descriptions'] = other_descriptions

	# get the relevant deals
	div_mbody_pics = single_deal.find('div', 'mbody').find_all('div', 'blk_tw_pic')
	pics_list_len = len(div_mbody_pics)
	if (pics_list_len >= 1):
		relevant_deals = []
		for div_pic in div_mbody_pics:
			relevant_deal = {}
			div_pic_title = div_pic.find('div', 'img_wrap')['title']
			relevant_deal['rel_deal_title'] = div_pic_title
			div_pic_redirect = div_pic.find('div', 'wrap_content').find('a').get('href').encode('utf-8')
			relevant_deal['rel_deal_url'] = div_pic_redirect
			div_pic_url = image_src(div_pic.find('div', 'wrap_content').find('img'))
			# relevant_deal['rel_pic_url'] = div_pic_url
			div_pic_format = div_pic_url.split(".")[-1]
			div_prices = div_pic.find('p').get_text().encode('utf-8').split(' ')
			div_pre_price = div_prices[0]
			relevant_deal['rel_pre_price'] = div_pre_price
			div_cur_price = div_prices[1]
			relevant_deal['rel_cur_price'] = div_cur_price
			relevant_deals.append(relevant_deal)
			urllib.urlretrieve(div_pic_url, path + data_id + '_rel_' + escape_special_chars(div_pic_title[:100]) + '.' + div_pic_format)
		single_deal_data['relevant_deals'] = relevant_deals

	# append the current deal to the list
	deals_list.append(single_deal_data)

json_data['deals'] = deals_list
with open(folder_name + '/' + subtitle + '.json', 'wb') as outfile:
	json.dump(json_data, outfile, sort_keys=True)

