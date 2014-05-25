from bs4 import BeautifulSoup
import urllib, urllib2
import json
import re
from datetime import datetime
import os

#url='http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId=732278&source=118'
#url='http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId=544536&source=118'
#url='http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId=1472224&source=118'
#url='http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId=817730&source=118'
#url='http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId=1037767&source=118'



url_first='http://www1.macys.com/catalog/category/facetedmeta?edge=hybrid&parentCategoryId=26846&categoryId=27686&multifacet=true&sortBy=ORIGINAL&productsPerPage=40&BRAND=Calvin%20Klein&facetName=BRAND'
page_first=urllib2.urlopen(url_first).read()
jsondata_first = json.loads(unicode(page_first,"ISO-8859-1"))    ####unicode for some unicode error
url=[]
for id in jsondata_first['productIds']:   # create a list of url
    url.append('http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId='+str(id)+'&source=118')



def escape_special_chars(str):
    return str.replace('/', '|')
json_data={}
json_data["products"]=[]
print len(url)
u=0
while u<len(url):
	page=urllib2.urlopen(url[u]).read()
	u+=1
	jsondata = json.loads(unicode(page,"ISO-8859-1"))    ####unicode for some unicode error
	productinfo=jsondata['productThumbnail']

	# NAME
	name=productinfo['productDescription']
	print 'Name : ',name

	#COLOR
	colors=[]
	print 'Color : '
	for color in productinfo['colorFamily']:
	    colors.append(color)
	print color
    
	#PRICE    
	price={}
	for item in jsondata['priceInfo']:    
	    if 'Price' in item:
	        if jsondata['priceInfo'][item]!=0 and jsondata['priceInfo'][item]!=True and jsondata['priceInfo'][item]!=False:
	            price[item]=jsondata['priceInfo'][item]
	            print item,' : ',jsondata['priceInfo'][item]


	#WEB ID
	id=productinfo['ID']
	print 'Web ID : ',id

	#CATEGORY
	category=jsondata['categoryName']
	print 'Category : ', category

	#IMAGE URLS
	print 'imageURLs :'
	Before = 'http://slimages.macys.com/is/image/MCY/products/'
	imgeurl={}
	for item in productinfo['colorwayPrimaryImages']:
	    imgeurl[item]=Before+productinfo['colorwayPrimaryImages'][item]
	print imgeurl   

	#write data of json file##################	
	details={}
	details["ImageURL"]=imgeurl
	details["Price"]=price
	details["Web ID"]=id
	details["Name"]=name
	details["Category"]=category
	json_data["products"].append(details)
	###########################################


	# create a folder
	folder_name = str(datetime.now()).split(' ')[0]
	path = folder_name + "/img/"
	if not os.path.exists(path):
		os.makedirs(path)

	# create json file and write data into json file
	filename ='jsonscrap'
	with open(folder_name + '/' + filename + '.json', 'wb') as outfile:
		json.dump(json_data, outfile, sort_keys=True)
	print '#'*40


	# download image
	for img_src in imgeurl: 
		img_format = imgeurl[img_src].split(".")[-1]
		urllib.urlretrieve(imgeurl[img_src], path + id +name + '_'+ escape_special_chars(img_src)+'.' + img_format)
	
	print u,'/',len(url)

