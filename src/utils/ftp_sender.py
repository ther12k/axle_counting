from ftplib import FTP
from config import IP_FTP, USER_NAME, USER_PASSWD

def sending_file(file_name, server_path=None):
	'''
	sending file to ftp server
	Args:
		file_name = file name
		folder_name = folder name
	'''
	
	ftp = FTP(IP_FTP)
	ftp.login(USER_NAME, USER_PASSWD)
	if server_path is not None:
		try: 
			ftp.cwd(server_path)
		except:
			print('Cannot create folder')
			return False
	try:    
		ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))
		ftp.quit()
		return True
	except:
		print('Cannot send file')
		return False