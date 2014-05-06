from bs4 import BeautifulSoup

import urllib2
import re
from io import StringIO

urlfile=open("urllist.txt")
urlsfile=urlfile.read()
urllist=urlsfile.split("\n")


#write the products information into a bs4json.json
fileName = "bs4json.json"
w = open(fileName,'w')
w.write('''{
	"products":[\n''')



print "There are "+str(len(urllist))+ " items in the list."
i = 0
while i<len(urllist):
    url=urllist[i]
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    
    
	######### find Name ########
    
    h1=soup.find_all("h1",id = "productTitle", class_="productTitle")
    name=h1[0].get_text()
    print "Name : "+ name

	######### find Origin Price & Now Price ########
    
    P1=soup.find_all("div",class_="standardProdPricingGroup")
    P2=P1[0]
    P3=P2.find_all("span")
    OrigP = str(P3[0].get_text())
    NowP = str(P3[1].get_text())

	#remove the additional word before the number
    Op = re.search(r'[0-9].+',OrigP)
    Np = re.search(r'[0-9].+',NowP)
    print "Original Price : $" + Op.group(0)
    print "Now Price : $" + Np.group(0)

	#########find Web ID #########
    I1=soup.find_all("div",class_="productID")
    I2=I1[0].get_text()
    ID = re.search(r'[0-9].+',I2)
    print "Web ID : " + ID.group(0)

	######### find Category #######
    C1 = soup.find_all("div",id = "breadCrumbsDiv")
    C2 = C1[0]
    C3 = C2.find_all("a")
    category = C3[0].get_text()
    Category=category.encode('utf8')
    if '&' in Category:
        Category1= Category[0:Category.find('&')]
        Category2= Category[Category.find('&')+1:]
        insert4and='and'
        CategoryFinal=Category1+insert4and+Category2
        print CategoryFinal


    print "Category : "+ CategoryFinal

	######### find Colors and Image URLs ########
    CI1=soup.find_all("script", type="text/javascript", text=re.compile( 'MACYS.pdp.primaryImages' ))
    CI2 = StringIO(unicode(CI1))               # transfer to unicode which can be read by StringIO
    for line in CI2:
	    if 'MACYS.pdp.primaryImages[' in line:
        	CI3=str(line)                   #transfer from unicode to str, which can be ready by .find  
    
    CI4=eval(CI3[CI3.find('{'):CI3.find('}')+1])  #transfer from str to dict by using eval
    Before = 'http://slimages.macys.com/is/image/MCY/products/'
    imgurl = []
    print "Colors and Image URLs"
    a = 0
    while a < len(CI4):
        imgurl.append( Before + CI4.values()[a])
        print "Color : " + CI4.keys()[a]
        print "Image URLs : " + imgurl[a]
        a+=1
    print "*"*30
    
    ##################################################
    ######write the second part of bs4json.json#######
    ##################################################
    
    if i<len(urllist)-1:
        w.write('		{\n'
'			"Name":"'+str(name)+'",\n'
'			"Colors":"'+str(CI4.keys())+'",\n'
'			"OriginalPrice":"'+Op.group(0)+'",\n'
'			"NowPrice":"'+Np.group(0)+'",\n'
'			"WebID":"'+ID.group(0)+'",\n'
'			"ImageURL":"'+str(imgurl)+'",\n'
'           "Category":"'+CategoryFinal+'"\n'    #CatergorrFinal and imageUrl both have unicode problem
'		},\n')
    else:
        w.write('		{\n'
'			"Name":"'+str(name)+'",\n'
'			"Colors":"'+str(CI4.keys())+'",\n'
'			"OriginalPrice":"'+Op.group(0)+'",\n'
'			"NowPrice":"'+Np.group(0)+'",\n'
'			"WebID":"'+ID.group(0)+'",\n'
'			"ImageURL":"'+str(imgurl)+'",\n'
'           "Category":"'+CategoryFinal+'"\n'
'		}\n')
    i = i+1

#Out of the big loop and Write the third part of JSON8.json

w.write('''	]
}\n''')

w.close()











        
        









