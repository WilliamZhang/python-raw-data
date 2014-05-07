from bs4 import BeautifulSoup

import urllib2
import re
from io import StringIO

urlfile=open("urllist.txt")
urlsfile=urlfile.read().rstrip()
urllist=urlsfile.split("\n")





    
def single_good():
	######### find Name ########
    
    h1=soup.find_all("h1",id = "productTitle", class_="productTitle")
    name=h1[0].get_text().encode("utf-8")
    print "Name : "+ name

	######### find Origin Price & Now Price ########
    
    P1=soup.find_all("div",class_="standardProdPricingGroup")
    P2=P1[0]
    P3=P2.find_all("span")
    if len(P3)==1:     # Some goods don't have Special Price (Now Price)
        OrigP = str(P3[0].get_text())
        NowP = OrigP
    else:
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
    
    print "*"*50
    
    ##################################################
    ######write the second part of bs4json.json#######
    ##################################################
   
    w.write('		{\n'
'			"Name":"%s",\n'
'			"Colors":"%s",\n'
'			"OriginalPrice":"%s",\n'
'			"NowPrice":"%s",\n'
'			"WebID":"%s",\n'
'			"ImageURL":"%s",\n'
'            "Category":"%s"\n'% (name,CI4.keys(),Op.group(0),Np.group(0),id,imgurl,Category))
    w.write('		},\n')



def multi_goods():
    level1=soup.find_all("div",class_="memberProducts masterSwatchTemplates More_Items ")
    Number_in_set=len(level1)
    
    #########find Web ID (All goods share same web id) #########
    I1=soup.find_all("div",class_="productID")
    I2=I1[0].get_text()
    ID = re.search(r'[0-9].+',I2)
    id=ID.group(0).encode('utf-8')
    
    ######### find Category (All goods share same category)#######
    C1 = soup.find_all("div",id = "breadCrumbsDiv")
    C2 = C1[0]
    C3 = C2.find_all("a")
    category = C3[0].get_text()
    Category=category.encode('utf-8')

    
    ############Bellow is other information########
    
    q=0
    while q< Number_in_set:
        ######### find Name ########
        h1=level1[q].find_all("div",id = "prodName")
        name=h1[0].get_text().encode("utf-8")
        print "Name : "+ name
        
        ######### find Origin Price & Now Price ########
    
    	P1=level1[q].find_all("div",class_="productPrice")
    	P2=P1[0]
        P3=P2.find_all("span")
        if len(P3)==1:     # Some goods don't have Special Price (Now Price)
            OrigP = str(P3[0].get_text())
            NowP = OrigP
        else:
            OrigP = str(P3[0].get_text())
            NowP = str(P3[1].get_text())

	    #remove the additional word before the number
        Op = re.search(r'[0-9].+',OrigP)
        Np = re.search(r'[0-9].+',NowP)
        print "Original Price : $" + Op.group(0)
        print "Now Price : $" + Np.group(0)

        ########### print web id############
        print "Web ID : " + id
        
        ########### print category #########
        print "Category : "+ Category
        
        ######### find Colors and Image URLs ########
        CI1=soup.find_all("script", type="text/javascript", text=re.compile( 'MACYS.pdp.primaryImages' ))
        CI2 = StringIO(unicode(CI1))               # transfer to unicode which can be read by StringIO
        imgurllist =[]
    	for line in CI2:
	    	if 'MACYS.pdp.primaryImages[' in line:
        		imgurllist.append(str(line))                #transfer from unicode to str, which can be ready by .find  
        
        CI3 = imgurllist[q]    # q consistent with the big loop q
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
        print "*"*50
        
        ##################################################
    	######write the second part of bs4json.json#######
    	##################################################
   
    	
        w.write('		{\n'
	'			"Name":"%s",\n'
	'			"Colors":"%s",\n'
	'			"OriginalPrice":"%s",\n'
	'			"NowPrice":"%s",\n'
	'			"WebID":"%s",\n'
	'			"ImageURL":"%s",\n'
	'            "Category":"%s"\n'
	'		},\n' % (name,CI4.keys(),Op.group(0),Np.group(0),id,imgurl,Category))
	
        
        q+=1



#####write the products information into a bs4json.json
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
    P1=soup.find_all("div",class_="standardProdPricingGroup")
    if len(P1) != 0:
        single_good()
    else:
        multi_goods()
    print 'No. :'+str(i+1)+'/'+ str(len(urllist))
    i+=1    
    

    
#Out of the big loop and Write the third part of JSON8.json

w.write('''	]
}''')
w.close()

# remove the , at the end of json file
ckcomma=open(fileName,'r')
ck=ckcomma.read().split('\n')
ck[-3]=ck[-3][:-1]
ckcomma.close()
overwrite=open(fileName,'w')
for line in ck:
    overwrite.write(line +'\n')
overwrite.close()








        
        









