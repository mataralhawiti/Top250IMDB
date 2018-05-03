#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
mini project where I'm trying to learn scraping a website with BeautifulSoup lib,
store the data in MongoDB, then do some analysis and viz on the pulled data. 

To-do :
# scrape Top250 list from IMDB using Requests&BS4 modules
# Store the data in MongoDB
# use pymongo module to mainpulate data
# use Pandas, NumPy to analyze & plot data
# use IPython
# use Superset from Airbnb to viz the data
# use D3.js to viz the data
# try to do some fun stuff with NLP
'''

__author__ = 'Matar'
import sys
import os
import re
import json
import datetime
import requests
import unicodedata
from bs4 import BeautifulSoup
import pymongo

top_movies_list_url = 'http://www.imdb.com/chart/top'
main_url = 'http://www.imdb.com'
movie_url = main_url+'/title/'
location_url = '/locations?ref_=tt_dt_dt'
#movies_list = []

def make_request(url) :
	""" get top 250 movies list

	:parm url: main url for 
	:return: conent object
	"""
	try :
		r = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(e)
		print("something is wrong, I could not make a request")
		sys.exit(1)

	return r.content



def get_movies_titleid(content) :
	""" exampl : tt0072684 

	:parm content: calling make_request()
	:return: a list that contains movies titles
	"""
	# make soup
	soup = BeautifulSoup(content)
	titles = soup.find_all("div")

	titles_list = []

	for title in titles :
		if title.has_attr('data-titleid') : # check it div tag has att called "data-titleid"
			titles_list.append(title.get("data-titleid"))

	return titles_list


def get_movies_link(movies_titleid):
	""" get list of the full link for the movie page
		exampl : http://www.imdb.com/title/tt0072684

		:parm movies_titleid : list of all movies title id="titleYear
		return: list of movies links
	"""

	movies_links = []

	for movie in movies_titleid :
		movies_links.append(movie_url+movie)
		break

	return movies_links

def get_movie_name(links_list):

	names = []

	for link in links_list :
		r = make_request(link)
		soup = BeautifulSoup(r)
		name = soup.find_all("h1", {"itemprop":"name"})
		for n in name:
			names.append(n.text.encode('utf-8'))
	return names

def get_single_movie_Info(links_list):
	movie_info = {}
	mv_link = links_list[0]
	r = make_request(mv_link)
	soup = BeautifulSoup(r)
	#name = soup.find_all("h1", {"itemprop":"name"}) #-- return : [] , 	#print(name[0].text)

	name = soup.find("h1", {"itemprop":"name"}).text
	rank = soup.find(href="/chart/top?ref_=tt_awd").text 
	year = soup.find(id = "titleYear").text
	rating = soup.find(itemprop="ratingValue").text
	rating_Count = soup.find(itemprop="ratingCount").text.strip().replace(",","")
	gener_tm = soup.find_all("span", itemprop="genre")
	gener = []
	for i in gener_tm:
		gener.append(i.text)

	director_tm = soup.find_all(itemprop="director")
	director = []
	for i in director_tm:
		director.append(i.text.strip())

	creator_tm = soup.find_all(itemprop="creator")
	creator = []
	for i in creator_tm:
		creator.append(i.find(itemprop="name").text.strip())	

	actros_tm = soup.find_all(itemprop="actors")
	actors = []
	for i in actros_tm:
		actors.append(i.text.strip().replace(",",""))

	metascore = soup.find("div", {"class":"metacriticScore score_favorable titleReviewBarSubItem"}).text.strip()
	keywords_tm = soup.find_all("span", itemprop="keywords")
	keywords = []
	for i in keywords_tm:
		keywords.append(i.text)

	filming_locations_request = requests.get(mv_link+location_url)
	filming_locations_soup = BeautifulSoup(filming_locations_request.content)
	filming_locations_tm = filming_locations_soup.find_all("dt")
	filming_locations = []
	for i in filming_locations_tm :
		filming_locations.append(i.text.strip())

	Storyline = soup.find("div", {"class":"inline canwrap", "itemprop":"description"}).text.strip()
	tag = soup.find("div", {"class":"txt-block"}).text.replace("Taglines:","").strip()



	movie_info = {
		"rank" : int(re.sub(r'\D', "",rank)),
		"name": name,
		"year" : int(re.sub(r'\D', "",year)),
		"rating" : float(rating) ,
		"rating_Count" : int(rating_Count) ,
		"gener" : gener,
		"director" : director,
		"creator" : creator,
		"actors" : actors,
		"metascore" : int(metascore),
		"keywords" : keywords,
		"filming_locations" : filming_locations,
		"Storyline" : Storyline,
		"tag" : tag
	}
	print(json.dumps(movie_info,sort_keys=True, indent=4))

def main():
	r = make_request(top_movies_list_url)
	mov_titls = get_movies_titleid(r)
	lks = get_movies_link(mov_titls)
	
	print("getting moives name ..", datetime.datetime.now())
	print("------------------------------------------------")
	nms = get_single_movie_Info(lks)

	#nms = get_movie_name(lks)
	# print("printing movies names", datetime.datetime.now())
	# print(nms)
	# for i in nms :
	# 	print(i.text)
	

if __name__ == "__main__" :
	main()

"""


#print(title.get("data-titleid"))
#movie_url+title.get("data-titleid")
#movies_list.append(movie_url+title.get("data-titleid"))

# rk = soup.find_all("span", {"name":"rk"})


def get_movies_url(titles) :
	for title in titles :
		if title.has_attr('data-titleid') :
			movies_list.append(movie_url+title.get("data-titleid"))
	return movies_list


def get_movie_detls(mov_lst) :
	mov_lst = get_movies_url(titles)

	for mov in mov_lst :
		r = requests.get(mov)
		mov_tilt = soup.find("h1", {"itemprop","name"}).text
		break



#m = requests.get('http://www.imdb.com/title/tt0111161/')
#soup = BeautifulSoup(m.content, "lxml")
#mov_tilt = soup.find_all("div", {"class","title_wrapper"})
#mov_tilt = soup.find_all("h1", {"itemprop":"name"})

#div class="title_wrapper"

#print(mov_tilt)
#print(len(mov_tilt))

#for i in mov_tilt :
	#print(i.text.encode('utf-8'))

ur = []
w = 1
def get_movies_url1(movies_list) :
	for mv in movies_list :
		m = requests.get(movie_url+mv)
		s = BeautifulSoup(m.content, "lxml")
		d = s.find_all("h1", {"itemprop":"name"})
		for i in d :
			a = i.text.encode('utf-8')
			a = a[:-9]
			ur.append(a)

		#print(d.text.encode('utf-8'))

get_movies_url1(movies_list)


for i in ur :
	print(i)
	#return movies_list



#<h1 itemprop="name" class="">The Shawshank Redemption&nbsp;<span id="titleYear">(<a href="/year/1994/?ref_=tt_ov_inf">1994</a>)</span>            </h1>

# ranking
# for movie in movies_list :
# 	print(movies_list.index(movie), movie)

# for r in rk:
# 	if r.has_attr("data-value") :
# 		print(r.get("data-value"))










#titles = soup.find_all("div", {"class":"data-titleid"})
#titles = soup.find_all("data-titleid")
#titles = soup.find_all("div").attrs
#for title in titles :
	#print(title)

#titles = soup.div
# i = 0
# for title in titles :
# 	a = title.get("data-titleid")
# 	if a is not None :
# 		print(a)
# print(i)

# for title in titles :
# 	if title.has_attr('data-titleid') :
# 		print(title.get("data-titleid"))





#titles = soup.div['class']

#titles = soup.div
#print(titles)


#print(titles.attrs['data-titleid'])
#attrs['data-lat']


'''
ur = []
w = 1
def get_movies_url1(movies_list) :
	for mv in movies_list :
		m = requests.get(movie_url+mv)
		s = BeautifulSoup(m.content, "lxml")
		d = s.find_all("h1", {"itemprop":"name"})
		for i in d :
			a = i.text.encode('utf-8')
			a = a[:-9]
			ur.append(a)

		#print(d.text.encode('utf-8'))

get_movies_url1(movies_list)


for i in ur :
	print(i)
	'''

"""