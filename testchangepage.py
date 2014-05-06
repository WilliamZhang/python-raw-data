from bs4 import BeautifulSoup
import urllib2
import re

########### the problem is python always read Page 1, not the page I am browsing######

#url4good='http://www1.macys.com/shop/handbags-accessories/all-handbags/Pageindex,Sortby,Productsperpage/2,ORIGINAL,40?id=27686'
url4good='http://www1.macys.com/shop/handbags-accessories/all-handbags/Pageindex,Sortby,Productsperpage/4,ORIGINAL,40?id=27686'
gpage=urllib2.urlopen(url4good)
gsoup=BeautifulSoup(gpage)

gdiv=gsoup.find_all('a',class_='productThumbnailLink')
gfilt=[]     # create list for relevant bs4

#########  filtrate irrelevant item#####
for item in gdiv:
    gg= item.find_all('span')
    if len(gg)==0:
        gfilt.append(item)
        
gbefore='http://www1.macys.com'
print "There are " +str(len(gfilt))+" items per page."
#filename='goodlink40perpg.txt'
#w=open(filename,'w')
n=0
while n<len(gfilt):
    print str(n+1) + '/' + str(len(gfilt))
    print gfilt[n].get_text()   # these are the name of goods we want
    gafter=gfilt[n].get('href')
    glink=gbefore+gafter    # these are the links we want
    print glink
    n+=1