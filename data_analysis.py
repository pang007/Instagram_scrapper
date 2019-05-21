import pandas as pd
from datetime import datetime
import requests
import pytz
from io import BytesIO
from PIL import Image

def data_transformation(file):
	'''
	to combine df[date] and df[time] and turn it into a datetime obejct with time df['datime']
	'''
	df = pd.read_csv(file)
	df['datetime'] = df['date'] + ' ' + df['time']
	n = len(df)
	for i in range(n):
		df['datetime'][i] = datetime.strptime(df['datetime'][i], '%Y-%m-%d %H:%M')
	
	# add a color field to define color
	df['color'] = 0
	df['image'] = ''
	for i in range(n):
		# add the segment time
		if 0 <= df['datetime'][i].hour <= 6:
			df['color'][i] = 'red'
		elif 6 < df['datetime'][i].hour <= 12:
			df['color'][i] = 'green'
		elif 12 < df['datetime'][i].hour <= 18:
			df['color'][i] = 'blue'
		elif 18 < df['datetime'][i].hour <= 24:
			df['color'][i] = 'cyan'
		else:
			raise Exception("No such hour is found!")

		# get the array object of each picture
		url = df['photo_link'][i]
		response = requests.get(url)
		img = Image.open(BytesIO(response.content))
		df['image'][i] = img
	df.to_csv(file .strip('.csv')+ "_created.csv")
	return df


def date_time_format(date, time):
	'''
	1. Take in the date and time variable and convert it into a datetime format
	2. convert the time from utc time zone into hk timezone
	input: date in 'dd/mm/yyyy' string format
		   time in 'hh:mm:ss AM/PM' string format and in utc timezone
	output: an datetime object for easy analysis

	'''
	# to make the existing datetime as utc time format
	utc_timezone = pytz.timezone('UTC')
	result_time = datetime.strptime(' '.join([date, time]), '%d/%m/%Y %H:%M:%S %p')
	result_time = utc_timezone.localize(result_time)
	# to convert the time into hk timezone format
	hk_timezone = pytz.timezone('Asia/Hong_Kong')
	hk_result_time = result_time.astimezone(hk_timezone)
	return hk_result_time


