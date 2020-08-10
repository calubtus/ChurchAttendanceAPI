import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

def resource_path_base():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return base_path

def append_device_info(info):
		with open(resource_path("devices.txt"), "a+") as file:
			# file.seek(0) # Move read cursor to the start of file.
			# data = file.read(100) # Start a new line if file not empty
			# if len(data) > 0 :
			#     file.write("\n")
			file.write(str(info))
			file.write("\n")

def read_number_of_devices():
		with open(resource_path("devices.txt"), "r") as infile:
		    lines = infile.readlines()
		return lines

def delete_device_info(deviceIndex):
		lines = read_number_of_devices()		
		with open(resource_path("devices.txt"), "w") as outfile:
		    for pos, line in enumerate(lines):
		        if pos != deviceIndex:
		            outfile.write(line)		
	
def read_device_info():
	device_info = []
	with open(resource_path("devices.txt"), "r") as file:
		for device in file:
			device = eval(device)
			if len(device) > 0: # check for empty strings 
				device_info.append(device[0:3]) # remove the password
	return device_info

def read_device_ip():
	host_names = []
	with open(resource_path("devices.txt"), "r") as file:
		for device in file:
			device = eval(device)
			if len(device) > 0: # check for empty strings 
				host_names.append(device[1]) # obtain ip address
	return host_names

def read_device_names():
	device_names = []
	with open(resource_path("devices.txt"), "r") as file:
		for device in file:
			device = eval(device)
			if len(device) > 0: # check for empty strings 
				device_names.append(device[0]) # obtain ip address
	return tuple(device_names)

def read_device_id():
	device_info = []
	with open(resource_path("devices.txt"), "r") as file:
		for device in file:
			device = eval(device)
			if len(device) > 0: # check for empty strings 
				device_info.append(device[1:4]) # obtain device info
	return device_info
