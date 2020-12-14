""" MAIN

Created by Giovanni E. Bonaventura

"""


from INSTABOT import*
from function import*


bot = InstaBot()
bot.register_session()

#bot.login()

bot.search_tag('valencia')
#SCRAPING PAGINA
bot.find_href('#valencia',2000,0.3) 


#SCRAPING POST

name='#valencia'
folder_path = './{}'.format(name)
H=open( '{}/Hlink.txt'.format(folder_path), 'r' )
HLINK=H.readlines()
(df,D)=bot.info_post(HLINK[0][:-2])
for i in HLINK[1:]:
	try:
		(df,D)=bot.info_post(i[:-2], df, D)
	except Exception as e:
		save_file(df,name,'df')
		save_dict(D,name,'diccionario')
save_file(df,name,'df')
save_dict(D,name,'diccionario')
df.to_csv(''.format(name))
