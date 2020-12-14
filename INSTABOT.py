""" SCRAPING_INSTABOT

Created by Giovanni E. Bonaventura

"""


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
import time
import numpy
import os
from function import *
import pandas as pd

class InstaBot:

	def __init__(self, username='', password=''):

		self.username=username  
		self.password=password
		self.browser=webdriver.Chrome('./chromedriver')
		self.base_url='https://www.instagram.com'
		time.sleep(1)

	def register_session(self):
		executor_url =str(self.browser.command_executor._url)
		session_id = self.browser.session_id
		s=open('./last_session.txt','w')
		s.write("%s" % executor_url)
		s.write("\n%s" % session_id)
		self.base_url='https://www.instagram.com'

	def find_buttons(self, button_text):

		buttons = self.browser.find_elements_by_xpath("//*[text()='{}']".format(button_text))

		return buttons



	def wait(self,n):
		
		self.n=n
		A = numpy.random.rand(1)*4
		A=A+n
		time.sleep(A)

	def login(self):
		self.browser.get('https://www.instagram.com/accounts/login')
		self.wait(1)
		self.browser.find_element_by_name("username").send_keys(self.username)
		self.browser.find_element_by_name("password").send_keys(self.password)
		self.browser.find_elements_by_xpath("//div[contains(text(), 'Accedi')]")[0].click()
		self.wait(3)
		notifica=self.find_buttons('Non ora')
		if notifica:
			notifica[0].click()
		time.sleep(2)

	def nav_user(self,user):
		self.user=user
		self.browser.get('{0}/{1}'.format(self.base_url,self.user))
		self.wait(4)

	def search_tag(self, tag):
		self.tag=tag
		self.browser.get('{}/explore/tags/{}'.format(self.base_url,self.tag))

	def search_local(self, position): 
		self.position=position
		self.browser.get('{}/explore/locations/{}'.format(self.base_url,self.position))


	def infinite_scroll(self):


		#self.last_height = self.browser.execute_script("return document.body.scrollHeight")

		self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		self.wait(2)

		#self.new_height = self.browser.execute_script("return document.body.scrollHeight")

	def find_href(self,name,n_lim,h_lim,Hlink=[]):
		
		self.name=name
		#num_post=self.browser.find_element_by_class_name('g47SY').text
		#num_post=str_to_numeric(num_post)
		#print('scraping on '+ str(num_post))
		folder_path = './{}'.format(name)
		if not os.path.exists(folder_path):
			os.mkdir(folder_path)
		H=open( '{}/Hlink.txt'.format(folder_path), 'w' )
		ID=1
		n=0
		start=time.time()
		stop=60*60*h_lim
		while True:
			self.infinite_scroll()
			self.wait(1)
			img=None
			counter=1
			while not img:
				try:
					img=self.browser.find_elements_by_class_name('v1Nh3')
					self.wait(1)
				except Exception as e:
					pass
				if counter>10:
					counter=0
					break
				counter+=1
			try:
				for j in img:
					href=j.find_element_by_css_selector('a')
					l=href.get_attribute('href')
					if l not in Hlink:
						Hlink.append(l)
						H.write( "%s\n" % l )
						ID+=1
			except:
				pass
			n+=1
			if n==10:
				print(str(ID)+'post has been found')
				print('Minutes from start: '+str((time.time()-start)/60))
				n=0
			if ID>n_lim:
				break
			if time.time()-start > stop:
				break
		H.close()

	def info_post(self, hlink, df=pd.DataFrame(columns=['User','Date','Position','Position_href','ALT','N_like','N_comments','SRC','Hlink']), D=dict([])):
		self.browser.get(hlink)
		self.wait(3)

		try:
			Date=self.browser.find_element_by_css_selector('time').get_attribute('title')
		except Exception as e:
			Date='none'

		try:
			User=self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a').text
		except Exception as e:
			User='none'
		try:
			Position=self.browser.find_element_by_class_name('O4GlU').text	
		except Exception as e:
			Position='none'
		try:
			Position_href=self.browser.find_element_by_class_name('O4GlU').get_attribute('href')
			Position_href=Position_href.split('https://www.instagram.com/explore/locations/')[1]	
		except Exception as e:
			Position_href='none'
		try:
			N_like=self.browser.find_element_by_class_name('Nm9Fw')
			N_like=N_like.find_element_by_css_selector('span').text
		except Exception as e:
			N_like='none'
		try:
			comment_element=self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[3]/div[1]')
			comment_elements=comment_element.find_elements_by_css_selector('span')
			N_comments=str(len(comment_elements[1:]))
			comments=[]
			for c in comment_elements[1:]:
				comments.append(c.text)

		except Exception as e:
			N_comments='none'
			comments=[]
		try:
			img=self.browser.find_element_by_class_name('KL4Bh').find_element_by_css_selector('img')
			ALT=img.get_attribute('alt')
		except Exception as e:
			ALT='none'
		try:
			SRC=img.get_attribute('src')
		except Exception as e:
			SRC='none'

		df.loc[df.shape[0],:]=[User,Date,Position,Position_href,ALT,N_like,N_comments,SRC,hlink]

		D[hlink]=comments

		return df, D


	def info_profile(self,user,D=dict([])):
		self.nav_user(user)
		info=[]
		info.append(self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text)
		info.append(self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title'))
		info.append(self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text)
		try:
			info.append(self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/span').text)
		except:
			info.append('Encoding Error')
		return info

###########################################################################################

class ReusingInstaBot(InstaBot):

	def __init__(self, username=None, password=None):

		session=open('./last_session.txt','r')
		s=session.readlines()
		executor_url=s[0]
		session_id=s[1]
		self.browser = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
		self.browser.session_id = session_id
		self.base_url='https://www.instagram.com'

	def Reusing_find_href(self,name):

		Hlink=[]
		folder_path = './{}'.format(name)
		H=open( '{}/Hlink.txt'.format(folder_path), 'r' )
		HLINK=H.readlines()
		for i in HLINK[-15:]:
			Hlink.append(i[:-2])
		self.find_href(name,Hlink)

