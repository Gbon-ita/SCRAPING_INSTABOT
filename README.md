# SCRAPING_INSTABOT
INTRO
the objective of this project is the extraction of data regarding instagram posts
There are 3 python's codes:
	1-INSTABOT.py
	2-MAIN.py
	3-function.py

The first implements several basic functions for a bot class object,
the second shows an example of how these basic functions can be combined to extrapolate data
and third supports the second.



HOW DOES IT WORK:

The data extraction is carried out through the selenium library, a web test library, which can interact directly with the web source file.
it needs a drive to work.
The present drive is a drive that can be used with chrome version "78.0.3904.87"


METHODS:

register_session()
	 
	In case of bot error it gives the possibility to use the same web page, through the ReusingInstaBot () class, and resumes the work 		from where it was left

login()

	some data can only be extracted by logged in users

nav_user()/search_tag()/search_local()

	allows you to navigate respectively in the page of a user, a tag or a place

find_href()

	scrolls a page and extracts the url of each post on the page
	INPUT:
		name- name of the folder that will be created
		n_lim- limit number of posts to extract
		h_lim- limit of hours dedicated to the extraction of posts
		Hlink- default value 0, accepts a list of URLs as input to avoid pulling the same post twice
	OUTPUT:
		./name/Hlink.txt- txt file with URLs of posts

info_post()

	scrolls a page and extracts the url of each post on the page
	INPUT:
		hlink- URL of post's page
	OUTPUT:
		df- dataframe with post's informations
		    ['User','Date','Position','Position_href','ALT','N_like','N_comments','SRC','Hlink'] 
		D- dictionary with key-value pair {hlink:list_of_comments}

info_profile()

	create or add key-value pair to a dictionary: {username: post number, follower number, follow number, bio}


the others support the methods listed above
