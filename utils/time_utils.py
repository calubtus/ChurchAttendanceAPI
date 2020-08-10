from datetime import datetime
  
def obtain_time():
	daytime = str(datetime.now())

	# Remove special characters
	daytime = daytime.replace(':','_')
	daytime = daytime.replace(' ','_')
	daytime = daytime.replace('-','_')
	daytime = daytime.replace('.','_')
	return daytime
