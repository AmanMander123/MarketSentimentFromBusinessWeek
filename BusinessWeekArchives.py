#Required packages
import sqlite3
import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import sys
import csv
import requests as rq
from bs4 import BeautifulSoup as bsoup

#READ SENTIMENT FILE
sent_file = open('AFINN-111.txt')
scores = {}
for line in sent_file:
	term, score = line.split("\t")
	scores[term] = int(score)
	
#Initialize settings for web scraping
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#Make array of dates
date_array = ['1991-01','1991-02','1991-03','1991-04','1991-05','1991-06','1991-07','1991-08','1991-09','1991-10','1991-11','1991-12',
'1992-01','1992-02','1992-03','1992-04','1992-05','1992-06','1992-07','1992-08','1992-09','1992-10','1992-11','1992-12',
'1993-01','1993-02','1993-03','1993-04','1993-05','1993-06','1993-07','1993-08','1993-09','1993-10','1993-11','1993-12',
'1994-01','1994-02','1994-03','1994-04','1994-05','1994-06','1994-07','1994-08','1994-09','1994-10','1994-11','1994-12',
'1995-01','1995-02','1995-03','1995-04','1995-05','1995-06','1995-07','1995-08','1995-09','1995-10','1995-11','1995-12',
'1996-01','1996-02','1996-03','1996-04','1996-05','1996-06','1996-07','1996-08','1996-09','1996-10','1996-11','1996-12',
'1997-01','1997-02','1997-03','1997-04','1997-05','1997-06','1997-07','1997-08','1997-09','1997-10','1997-11','1997-12',
'1998-01','1998-02','1998-03','1998-04','1998-05','1998-06','1998-07','1998-08','1998-09','1998-10','1998-11','1998-12',
'1999-01','1999-02','1999-03','1999-04','1999-05','1999-06','1999-07','1999-08','1999-09','1999-10','1999-11','1999-12',
'2000-01','2000-02','2000-03','2000-04','2000-05','2000-06','2000-07','2000-08','2000-09','2000-10','2000-11','2000-12',
'2001-01','2001-02','2001-03','2001-04','2001-05','2001-06','2001-07','2001-08','2001-09','2001-10','2001-11','2001-12',
'2002-01','2002-02','2002-03','2002-04','2002-05','2002-06','2002-07','2002-08','2002-09','2002-10','2002-11','2002-12',
'2003-01','2003-02','2003-03','2003-04','2003-05','2003-06','2003-07','2003-08','2003-09','2003-10','2003-11','2003-12',
'2004-01','2004-02','2004-03','2004-04','2004-05','2004-06','2004-07','2004-08','2004-09','2004-10','2004-11','2004-12',
'2005-01','2005-02','2005-03','2005-04','2005-05','2005-06','2005-07','2005-08','2005-09','2005-10','2005-11','2005-12',
'2006-01','2006-02','2006-03','2006-04','2006-05','2006-06','2006-07','2006-08','2006-09','2006-10','2006-11','2006-12',
'2007-01','2007-02','2007-03','2007-04','2007-05','2007-06','2007-07','2007-08','2007-09','2007-10','2007-11','2007-12',
'2008-01','2008-02','2008-03','2008-04','2008-05','2008-06','2008-07','2008-08','2008-09','2008-10','2008-11','2008-12',
'2009-01','2009-02','2009-03','2009-04','2009-05','2009-06','2009-07','2009-08','2009-09','2009-10','2009-11','2009-12',
'2010-01','2010-02','2010-03','2010-04','2010-05','2010-06','2010-07','2010-08','2010-09','2010-10','2010-11','2010-12',
'2011-01','2011-02','2011-03','2011-04','2011-05','2011-06','2011-07','2011-08','2011-09','2011-10','2011-11','2011-12',
'2012-01','2012-02','2012-03','2012-04','2012-05','2012-06','2012-07','2012-08','2012-09','2012-10','2012-11','2012-12',
'2013-01','2013-02','2013-03','2013-04','2013-05','2013-06','2013-07','2013-08','2013-09','2013-10','2013-11','2013-12']

#Initialize score
total_scores = {}
#Loop over all dates
for current_date in date_array:
	#Link to Business Week archives
	main_url = "http://www.businessweek.com/archive/"+current_date+"/news.html"
	r = rq.get(main_url)
	
	#Use beautiful soup to load content
	soup = bsoup(r.content)
	
	#Extract links to the articles
	g_data = soup.find_all("ul",{"class":"weeks"})
	links_messy_headlines = str(g_data[0].find_all('a'))
	links_headlines = re.findall(r'<a href=\"(.*?)\"', links_messy_headlines)
	monthscore = 0
	for url in links_headlines:
		print ('***************************************************************')
		print url
		try:	
			#Go to each article link to scrape
			r = rq.get(url)
			soup_headlines = bsoup(r.content)
			h_data = soup_headlines.find_all("ul",{"class":"archive"})
			links_messy = str(h_data[0].find_all('a'))
			links = re.findall(r'<a class="headline" href=\"(.*?)\"', links_messy)
			for link in links:
				r = rq.get(link)
				soup_article = bsoup(r.content)
				article_data = str(soup_article.find_all("div",{"id":"article_body"}))
				body = re.findall(r'<p>(.*?)</p>', article_data)
				one_body = ''.join(body)
				one_body = one_body.lower()
				words = one_body.split()
				for word in words:
					if word in scores:
						monthscore += scores[word]
						monthscore += 0.0
				print current_date
				print monthscore
		except:
			pass
	total_scores[current_date] = monthscore

#Write output file
resultFile = open("Sentoutput.csv",'wb')
wr = csv.writer(resultFile, dialect='excel')
for key, value in total_scores.items():
	wr.writerow([key, value])
	
