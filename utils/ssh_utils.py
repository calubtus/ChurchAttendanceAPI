import pysftp
import sys
import paramiko
import os.path

from utils import device_utils as dev_utils

def sftp_service():
	device_info = dev_utils.read_device_id()
	KNOWN_HOSTS_PATH = os.path.expanduser('~/.ssh/known_hosts')
	IMAGES_PATH  = dev_utils.resource_path_base() + "\\system_images"
	PICAMERA_DIR = "church_images"
	cnopts = pysftp.CnOpts()
	cnopts.hostkeys.load(KNOWN_HOSTS_PATH)

	for device in device_info:
		try:
			with pysftp.Connection(host=device[0], username=device[1], password=device[2], cnopts=cnopts) as sftp:
				if not sftp.isdir(PICAMERA_DIR):
					print("creating directiry...")
					sftp.mkdir(PICAMERA_DIR)
				sftp.get_d(PICAMERA_DIR, IMAGES_PATH)
		except pysftp.SSHException:
		    print("unable to connect device...")
		    return False
	return True

def create_ssh_key():
	KNOWN_HOSTS_PATH = os.path.expanduser('~/.ssh/known_hosts')
	SSH_FOLDER_PATH = os.path.expanduser('~/.ssh')

	if not os.path.exists(SSH_FOLDER_PATH):
	    os.makedirs(SSH_FOLDER_PATH)

	host_names = dev_utils.read_device_ip()
	device_info = dev_utils.read_device_info()

	for index, host in enumerate(host_names):
		address = host+':'+'22'

		if os.path.isfile(KNOWN_HOSTS_PATH):
		    known_hosts = KNOWN_HOSTS_PATH
		else:
		    open(KNOWN_HOSTS_PATH, 'w').close()
		    known_hosts = KNOWN_HOSTS_PATH

		try: 
			transport = paramiko.Transport(address)
		except pysftp.SSHException:
			print("unable to connect device to %s..." % (host))
			dev_utils.delete_device_info(index)
			return False, device_info[index][0] #Unable to make connection with device
		
		transport.connect()
		key = transport.get_remote_server_key()
		transport.close()

		hostfile = paramiko.HostKeys(filename=known_hosts)
		hostfile.add(hostname = host, key=key, keytype=key.get_name())

		hostfile.save(filename=known_hosts)
	return True, None # Able to make connection with all devices
