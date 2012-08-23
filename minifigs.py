
import pymongo
from pymongo import Connection
import urllib
import re
from bs4 import BeautifulSoup 

conn = Connection("localhost")
db = conn.test
coll = db.Minifigs

def getURL(url):
	sock = urllib.urlopen(url)
	data = sock.read()
	sock.close
	return data

def catParser(page):

	plinks = []
	try:
		d = getURL(page)
	except:
		return plinks
	
	soup = BeautifulSoup(d)
	all_links = soup.find_all('a')
	
	for link in all_links:
		pdoc = {}
		if link["href"].find("catalogItem.asp?S") >= 0:
			set = str(link["href"]).split("=")[1]
			link = "http://www.bricklink.com/"+str(link["href"])
			pdoc = {"id":set,"link":link}
			plinks.append(pdoc)

	return plinks

def comParser(page):

	plinks = []
	try:
		d = getURL(page)
	except:
		return plinks
	
	soup = BeautifulSoup(d)
	all_links = soup.find_all('a')
	
	for link in all_links:
		pdoc = {}
		if link["href"].find("catalogItem.asp?P") >= 0:
			set = str(link["href"]).split("=")[1]
			link = "http://www.bricklink.com/"+str(link["href"])
			pdoc = {"id":set,"link":link}
			plinks.append(pdoc)

	return plinks

def ParseInsertData():

	# file is tab delimited in this form:
	# Category ID	Category Name	Number	Name	Weight (in Grams)

	f = open('/Users/kennygorman/Downloads/Minifigs.txt', 'r')

	for line in f:
	  doc = {}
	  line = line.rstrip()
	  a = line.split('\t')
	  doc["categoryID"] = a[0]
	  doc["categoryName"] = a[1]
	  doc["itemNumber"] = a[2]
	  doc["itemName"] = a[3]
	  doc["imageLargeURL"] = "http://www.bricklink.com/ML/%s.jpg" % (a[2])
	  doc["imageThumbURL"] = "http://img.bricklink.com/M/%s.gif" % (a[2])
	  doc["tags"] = a[1].split('/')
	  try:
	   	float(a[4])
		doc["itemWeightGrams"] = float(a[4])
	  except:
	   	doc["itemWeightGrams"] = None

	  lookupPage = "http://www.bricklink.com/catalogItemIn.asp?M=%s&v=0&in=S&srt=0&srtAsc=A&ov=Y" % (a[2])
	  out = catParser(lookupPage)
	  if out:
	  	doc["sets"] = out

	  lookupPage = "http://www.bricklink.com/catalogItemInv.asp?M=%s" % (a[2])
	  out = comParser(lookupPage)
	  if out:
	  	doc["components"] = out

	  coll.insert(doc)

if __name__ == "__main__":
 	ParseInsertData()