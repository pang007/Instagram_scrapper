# this is to scrap the info from multiple account at the same time

from ig_scrapper import IGScrapper
import argparse
from data_analysis import data_transformation
from data_plot import plot_scroll_annotate_bar_chart
import threading

# input username in a list and corresponding ig password in a list
# length of below list should be the same
username_list = ['<username to be added>']
password_list = ['<password to be added>']
username_to_be_scrapped = ['<username to be scrapped>']
scrapper_dict = {}

if __name__ == "__main__":

	if len(username_list) != len(password_list) or len(password_list) != len(username_to_be_scrapped):
		raise IndexError('Lenght of username list, password list or username to be scrapped list not match!')
	
	# run the major code
	i = 0
	for username, password in zip(username_list, password_list):
		scrapper_dict[i] = IGScrapper(username, password)
		i += 1

	for  a , username in enumerate(username_list):
		threading.Thread(target = scrapper_dict[a].scrap_all_post_info, args = (username_to_be_scrapped[a],)).start()
		time.sleep(1) # to avoid the same login time for multiple accounts at your IP


