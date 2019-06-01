from ig_scrapper import IGScrapper
import argparse
from data_analysis import data_transformation
from data_plot import plot_scroll_annotate_bar_chart


if __name__ == "__main__":
	# for command line argument usage
	parser = argparse.ArgumentParser()

	# add the first command line argument as the username, password and username to be scrapped
	parser.add_argument("username", help='enter your instagram username', type=str, required = True)
	parser.add_argument("password", help='enter your instagram password', type=str, required = True)
	parser.add_argument("scrap_username", help='enter username that you want to scrap in instagram', type=str, required = True)
	args = parser.parse_args()
	username = args.username
	password = args.password
	username_to_be_scrapped = args.scrap_username

	# run the major code
	lentaa = IGScrapper(username, password)
	lentaa.scrap_all_post_info(username_to_be_scrapped)
	df = data_transformation(filename + '_' + username_to_be_scrapped + '.csv')
	plot_scroll_annotate_bar_chart(df)
