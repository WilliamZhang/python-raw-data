#This add different categories, and checking system
#This is mainly using json method, and using Bs4 method to modify errors in json
from bs4 import BeautifulSoup
import urllib, urllib2
import json
import re
from datetime import datetime
import os
from io import StringIO



####json method####
def json_single():
    productinfo=jsondata['productThumbnail']

    # NAME
    name=productinfo['productDescription']
    print 'Name : ',name

    #COLOR
    colors=[]
    print 'Color : '
    for color in productinfo['colorFamily']:
        colors.append(color)
    print colors
    
    #PRICE    
    price={}
    for item in jsondata['priceInfo']:    
        if 'Price' in item and 'base' not in item:
            if jsondata['priceInfo'][item]!=0 and jsondata['priceInfo'][item]!=True and jsondata['priceInfo'][item]!=False:
                price[item]=str(jsondata['priceInfo'][item])
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

    print type(productinfo['colorwayPrimaryImages'])
    print productinfo['colorwayPrimaryImages']
    
    for item in productinfo['colorwayPrimaryImages']:
        imgeurl[item]=Before+productinfo['colorwayPrimaryImages'][item]

    if len(imgeurl)==0:    #some goods like bed do not have colowayPrimaryImages
        imgeurl["Main_Image"]=Before+productinfo["imageSource"]
            
    print imgeurl   
    
    #########Above are basic information##########
    #########Below are additinoal information #####
    # size for shoes or jeans and so on
    size = []
    print "Size :"
    if "sizes" in productinfo.keys():
        for item in productinfo['sizes']:
            size.append(item)
    print size
    
    #gender: exist in general, absence in bed stuff and so on
    gender=[]
    print "Gender :"
    attr=productinfo["attributes"]
    if "GENDER" in productinfo["attributes"].keys():
        for item in productinfo["attributes"]["GENDER"]:
            gender.append(item)
    print gender





    #write data of json file##################  
    details={}
    details["ImageURL"]=imgeurl
    details["Price"]=price
    details["Web ID"]=id
    details["Name"]=name
    details["Category"]=category
    details["Color"]=colors

    details["Size"]=size
    details["Gender"]= gender
    #check wether the keys in detail[] are empty 
    for key in details.keys():
        if len(details[key])==0:
            del details[key]

    json_data["products"].append(details)
    ###########################################


    # create json file and write data into json file
    filename ='jsonscrap'
    with open(folder_name + '/' + filename + '.json', 'wb') as outfile:
        json.dump(json_data, outfile, sort_keys=True)
 


    # download image, img_src has different colors which like Black/White, we should transfer it into Black|White
    for img_src in imgeurl: 
        img_format = imgeurl[img_src].split(".")[-1]
        urllib.urlretrieve(imgeurl[img_src], path + id +escape_special_chars(name) + '_'+ escape_special_chars(img_src)+'.' + img_format)









#####Bs4 method#####
def single_good():
    ######### find Name ########
    h1=soup.find_all("h1",id = "productTitle", class_="productTitle")
    if len(h1)==0:print "not exsit"     #check the existence of the good

    name=h1[0].get_text().encode("utf-8")
    print "Name : "+ name

    ######### find Origin Price & Now Price ########
    
    P1=soup.find_all("div",class_="standardProdPricingGroup")
    P2=P1[0]
    P3=P2.find_all("span")

    print "Price"
    price = {}
    for item in P3:
    	if "$" in item.get_text():
    		p=item.get_text().encode("utf-8")
    		PriceSubject=p[0:p.find("$")]
    		P=p[p.find("$")+1:-1]
    		if "Orig." in PriceSubject:     # making the price tag constent with that in json source
    			PriceSubject="originalPrice"
    		elif "Was" in PriceSubject:
    			PriceSubject="wasPrice"
    		elif "Now" in PriceSubject:
    			PriceSubject="salePrice"
    		elif PriceSubject=="":
    			PriceSubject="salePrice"
    		elif "Reg." in PriceSubject:
    			PriceSubject="regPrice"
    		elif "Sale" in PriceSubject:
    			PriceSubject="salePrice"
    		elif "ur" in PriceSubject:
    			PriceSubject="ourPrice"
    		elif "et" in PriceSubject:
    			PriceSubject="retailPrice"
        price[PriceSubject]=P
    print price 


    #########find Web ID #########
    I1=soup.find_all("div",class_="productID")
    I2=I1[0].get_text()
    ID = re.search(r'[0-9].+',I2)
    id=ID.group(0).encode('utf-8')
    print "Web ID : " + ID.group(0)

    ######### find Category #######
    C1 = soup.find_all("div",id = "breadCrumbsDiv")
    C2 = C1[0]
    C3 = C2.find_all("a")
    category = C3[0].get_text()
    Category=category.encode('utf-8')
    print "Category : "+ Category

    ######### find Colors and Image URLs ########
    CI1=soup.find_all("script", type="text/javascript", text=re.compile( 'MACYS.pdp.primaryImages' ))
    CI2 = StringIO(unicode(CI1))               # transfer to unicode which can be read by StringIO
    for line in CI2:
        if 'MACYS.pdp.primaryImages[' in line:
            CI3=str(line)                   #transfer from unicode to str, which can be ready by .find 
        if 'MACYS.pdp.productLvlPrimary' in line:       
            CI6=str(line)
            CI7=CI6[CI6.find('"')+1:-3] 
    
    CI4=eval(CI3[CI3.find('{'):CI3.find('}')+1])  #transfer from str to dict by using eval

    Before = 'http://slimages.macys.com/is/image/MCY/products/'
    imgurl = {}
    colors=[]
    print "Colors and Image URLs"
    a = 0
    while a < len(CI4):
        imgurl[CI4.keys()[a]]=( Before + CI4.values()[a])
        colors.append(CI4.keys()[a])
        print "Color : " + CI4.keys()[a]
        print "Image URLs : " + imgurl[CI4.keys()[a]]
        a+=1
    
    if len(imgurl)==0:     #some goods like bed do not have colowayPrimaryImages
        imgurl["Main_Image"]=Before+CI7

    print imgurl

    #########Above are basic information##########
    #########Below are additinoal information #####
    # size for shoes or jeans and so on
    size = []
    sizediv = soup.find_all('div',id='printableSizes')
    if len(sizediv) != 0:     # check the existence of size
        Size=sizediv[0].get_text().encode("utf-8")
        sizesplit=Size.split(",")
        for item in sizesplit:
            size.append(item.strip())
    print "Size : "
    print size
    

    #gender: exist in general, absence in bed stuff and so on
    #some problem with this way, cannot find exact info about gender in page
    #gender=[]
    #print "Gender :"
    #genderspan=soup.find_all("span",itemprop="gender",class_="userstyleBold") # first reviewer's gender
    #if len(genderspan)!=0:
    #    Gender=genderspan[0].get_text().encode("utf-8")
    #    gender.append(Gender)
    #print gender


    #write data of json file##################  
    details={}
    details["ImageURL"]=imgurl
    details["Price"]=price
    details["Web ID"]=id
    details["Name"]=name
    details["Category"]=Category
    details["Color"]=colors

    details["Size"]=size
    #details["gender"]=gender
    #check wether the keys in detail[] are empty 
    for key in details.keys():
        if len(details[key])==0:
            del details[key]

    json_data["products"].append(details)
    ###########################################

    # create json file and write data into json file
    filename ='jsonscrap'
    with open(folder_name + '/' + filename + '.json', 'wb') as outfile:
        json.dump(json_data, outfile, sort_keys=True)

    # download image, img_src has different colors which like Black/White, we should transfer it into Black|White
    for img_src in imgurl: 
        img_format = imgurl[img_src].split(".")[-1]
        urllib.urlretrieve(imgurl[img_src], path + id +escape_special_chars(name) + '_'+ escape_special_chars(img_src)+'.' + img_format)
    

        

def multi_goods():
	#level1=soup.find_all("div",class_="memberProducts masterSwatchTemplates More_Items ")
	level1=soup.find_all("div",class_=re.compile("memberProducts"))
	print "Collectoin Goods: "+str(len(level1))
	if len(level1) != 0:
		A.append(URL)
		for member in level1:
			goodmember=member.get("id").encode("utf-8")
			goodid=re.search(r'[0-9].+',goodmember)  #find id of each good in collection
			collectionUrls.append('http://www1.macys.com/shop/search?keyword='+goodid.group(0))
	else:
		FinalError.append(URL)
		



def escape_special_chars(str):
    return str.replace('/', '|')



#############################################################
#############################################################
#############################################################
#####Find URL for json method################################

#Url="http://www1.macys.com/shop/handbags-accessories/all-handbags?id=27686&edge=hybrid&cm_sp=us_hdr-_-handbags-%26-accessories-_-27686_all-handbags"
#Url="http://www1.macys.com/shop/shoes/all-womens-shoes?id=56233&edge=hybrid&cm_sp=us_hdr-_-shoes-_-56233_all-women%27s-shoes"
#Url="http://www1.macys.com/shop/bed-bath/down-comforters?id=28898&edge=hybrid&cm_sp=us_catsplash_bed-%26-bath-_-row4-_-category_1-save-50%25-plus-extra-20%25-off-comforters-"
#Url="http://www1.macys.com/shop/furniture/lowest-prices-of-the-season?id=44966&edge=hybrid&cm_sp=us_catsplash_furniture-_-row5-_-category_1-lowest-prices-of-the-season-on-select-furniture&cm_kws_path=758798"
#Url="http://www1.macys.com/shop/jewelry-watches/mens-watches?id=57386&edge=hybrid&cm_sp=us_hdr-_-jewelry-%26-watches-_-57386_men%27s-watches"
#Url="http://www1.macys.com/shop/beauty-perfume-and-makeup/makeup?id=30077&edge=hybrid&cm_sp=us_hdr-_-beauty-_-30077_makeup"
#Url="http://www1.macys.com/shop/jewelry-watches/all-diamond-jewelry?id=57702&edge=hybrid&cm_sp=us_hdr-_-jewelry-%26-watches-_-57702_shop-all-diamonds"
#Url="http://www1.macys.com/shop/mens-clothing/mens-jeans?id=11221&edge=hybrid&cm_sp=us_hdr-_-men-_-11221_jeans"
#Url-"http://www1.macys.com/shop/mattresses?id=25931&edge=hybrid&cm_sp=us_hdr-_-for-the-home-_-25931_mattresses"
#Url="http://www1.macys.com/shop/bed-bath/beach-towels?id=51717&edge=hybrid&cm_sp=us_hdr-_-bed-%26-bath-_-51717_beach-towels"
#Url="http://www1.macys.com/shop/bed-bath/ralph-lauren?id=65577&edge=hybrid&cm_sp=us_hdr-_-bed-%26-bath-_-65577_ralph-lauren"
#Url="http://www1.macys.com/shop/handbags-accessories/womens-sunglasses?id=28295&edge=hybrid&cm_sp=us_hdr-_-handbags-%26-accessories-_-28295_sunglasses"
Url="http://www1.macys.com/shop/handbags-accessories/belts?id=27807&edge=hybrid&cm_sp=us_hdr-_-handbags-%26-accessories-_-27807_belts"
page = urllib2.urlopen(Url)
soup = BeautifulSoup(page)
Allid= soup.find_all("script",type ="text/javascript")

for item in Allid:
    if "MACYS.colorwayPrimaryImages" in item.get_text():
        idarea= item.get_text()

idareasplit=idarea.split(";")
for item in idareasplit:      # find id of each product in the category front page
    if "MACYS.colorwayPrimaryImages" in item:
        a=item[item.find("=")+4:-2]
        s="'"+a+"'"
        dic=json.loads(a)

url=[]
for id in dic.keys():   # create a list of url
    url.append('http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId='+str(id)+'&source=118')



# create a folder and several important lists
folder_name = str(datetime.now()).split(' ')[0]
path = folder_name + "/img/"
if not os.path.exists(path):
    os.makedirs(path)

json_data={}
json_data["products"]=[]
print len(url)

Errorlist=[]    #this list is derived from json method, then be used by Bs4 method
collectionUrls=[]  # this list is derived from Bs4 multiple method to make single urls for the goods in collection, these urls could be used by Bs4 single method
FinalError=[]    # this list is the final Urls could not be read and write into json file
goodCOUNT=0    #record how many goods in the whole process
timeCOUNT=0    #show the process of running
A=[]  # A is the url of collection
################################
#start work by using json method
u=0
while u<len(url):
    page=urllib2.urlopen(url[u]).read()
    u+=1
    jsondata = json.loads(unicode(page,"ISO-8859-1"))    ####unicode for some unicode error
    if jsondata['productThumbnail']==None :      ####check the validation of the url
        modifyurl=url[u-1][url[u-1].find("=")+1:url[u-1].find("&")]
        Errorlist.append('http://www1.macys.com/shop/search?keyword='+modifyurl) #write into Errorlist for Bs4 method
        timeCOUNT+=1
        print "JSON (invalid): "+str(timeCOUNT)+"/"+str(len(url))
        print "*"*40
        continue

    if len(jsondata['productThumbnail']['childProductIds'])!=0:   #### =0 for single, !=0 for collection good 
        A.append(url[u-1])    # u+1 before, so -1 should be applied
        for id in jsondata['productThumbnail']['childProductIds']:     # write into url[] for redoing json method
            url.append('http://www1.macys.com/shop/catalog/product/newthumbnail/json?productId='+str(id)+'&source=118')
        timeCOUNT+=1
        print "JSON (collection): "+str(timeCOUNT)+"/"+str(len(url))   
        print "*"*40
        continue

    json_single()  ##### using json method
    goodCOUNT+=1
    timeCOUNT+=1
    print "JSON : "+str(timeCOUNT)+"/"+str(len(url))
    print "*"*40

# using Bs4 method to fix errors
i=0
while i<len(Errorlist):
	URL=Errorlist[i]
	i+=1
	print URL
	page=urllib2.urlopen(URL)
	soup = BeautifulSoup(page)
	P1=soup.find_all("div",class_="standardProdPricingGroup")
	if len(P1) != 0:   #check wthether be single good
		single_good()   #Using function of single
		goodCOUNT+=1
		timeCOUNT+=1

	else:
		multi_goods()   #using function of multi to make collectionUrls[], for redoing single method
		timeCOUNT+=1
	print "SINGLE : "+str(timeCOUNT)+"/"+str(len(url)+len(Errorlist)+len(collectionUrls))
	print "*"*40

#read and write colletion
c=0
while c<len(collectionUrls):
	Url=collectionUrls[c]
	c+=1
	print Url
	page=urllib2.urlopen(Url)
	soup = BeautifulSoup(page)
	P1=soup.find_all("div",class_="standardProdPricingGroup")
	if len(P1) != 0:
		single_good()
		goodCOUNT+=1
		timeCOUNT+=1
	else:
		FinalError.append(Url)
		timeCOUNT+=1
		continue     # if single good only in collection page, ignore it
	print "COLLECTION : "+str(timeCOUNT)+"/"+str(len(url)+len(Errorlist)+len(collectionUrls))
	print "*"*40
print "*************Summary*************"
print "Total number:"
print "Single goods: %d, Collection : %d \n" %(goodCOUNT, len(A))
print "Collection Urls :"
print A   # the list of url of collection
print "\nNumber of errors in Json method (including single goods and collection):"+str(len(Errorlist))
print "\nFinal Error : "
print FinalError
print "*"*40













