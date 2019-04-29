# Instagram_scrapper

This is a script to scrape instagram data based on selenium and beautiful soup of python.

It can scrap the input user's all post website linke, post img, number of like and date and time of the post and export it into a csv file.

Usage is very easy. In the ig_scrapper.py file, at the bottom, there is 
	username = '<username input>'
	password = '<passowrd input>'
	filename = 'ig_scrapper'
	driver_type = 'chrome'
	username_to_be_scrapped = '<username to be scrapped>'
	lentaa = IGScrapper(username, password, filename, driver_type)
	lentaa.scrap_all_post_info(username_to_be_scrapped)
  
  you have to input the '<username input>', '<passowrd input>' and '<username to be scrapped>' and run the code.
  
  
