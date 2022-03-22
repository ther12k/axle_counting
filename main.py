import cv2
import time
from src import MainProcess
from adam_io import DigitalOutput
from src.utils import Adam6050DInput
from src.utils.camera import Camera
from adam_io import DigitalOutput

from src.utils import logging, datetime_format
from config import DEVICE_ID, GATE_ID, TIMEID_FORMAT,FTP_HOST, USER_NAME, USER_PASSWD
import ftplib
from datetime import datetime
import os

class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=0)
		self.camera_run  	= self.camera.run()
		self.adam			= Adam6050DInput()
		self.app         	= MainProcess()
		self.prev_A1		= 1

	#prefer to move to another file	
	def chdir(self,ftp_path, ftp_conn):
		dirs = [d for d in ftp_path.split('/') if d != '']
		for p in dirs:
			self.check_dir(p, ftp_conn)

	#prefer to move to another file
	def check_dir(dir, ftp_conn):
		filelist = []
		ftp_conn.retrlines('LIST', filelist.append)
		found = False
		for f in filelist:
			if f.split()[-1] == dir and f.lower().startswith('d'):
				found = True

		if not found:
			ftp_conn.mkd(dir)
		ftp_conn.cwd(dir)

	def video_upload(self,time_id):
		try:
			name = time_id.strftime(TIMEID_FORMAT)[:-4]
			year, month, day, hour, _, _,_ = datetime_format()
			dest_path = f'/{GATE_ID}/{year}/{month}/{day}/'
			"""Transfer file to FTP."""
			# Connect
			session = ftplib.FTP(FTP_HOST, USER_NAME, USER_PASSWD)

			# Change to target dir
			self.chdir(dest_path,session)

			# Transfer file
			file_name = name+'.avi'
			logging.info("Transferring %s to %s..." % (file_name,dest_path))
			with open('results/'+file_name, "rb") as file:
				session.storbinary('STOR %s' % os.path.basename(dest_path+file_name), file)
			
			# Close session
			session.quit()
			return dest_path+file_name
		except:
			logging.info('error: upload file error')
			return 'error: upload file error'

	def __write_video(self, time_id):
		size = (int(self.camera_run.get(4)), int(self.camera_run.get(3)))
		name = time_id.strftime(TIMEID_FORMAT)[:-4]
		ret = cv2.VideoWriter(f'results/{name}.avi',cv2.VideoWriter_fourcc(*'XVID'), 20, (1080,1920))

		return ret
	
	def run(self):
		while True:
			adam_inputs = self.adam.di_inputs()
			A1, A2 = adam_inputs[0][1], adam_inputs[1][1]
			B1, B2 = adam_inputs[2][1], adam_inputs[3][1]
			# Condition start recording and running app
			if self.prev_A1==1 and A1==0:
			#if A1==0 and A2==1 and B1==1 and B2==1:
				print('Start recording')
				time_now = datetime.now()
				self.adam.di_output(DigitalOutput(array=[0,1,0,0,0,0]))
				out_video =  self.__write_video(time_now)
				while True:
					adam_inputs = self.adam.di_inputs()
					A1, A2 = adam_inputs[0][1], adam_inputs[1][1]
					B1, B2 = adam_inputs[2][1], adam_inputs[3][1]
					ret, frame = self.camera_run.read()
					if not ret:
						self.camera.release(ret=False)
						self.capture = self.camera.run()
						time.sleep(1)
						continue
					else:
						file_path = self.video_upload(time_now)
						if 'error' in file_path :
							file_path=''
						drawed = self.app.main(frame,time_now,file_path)
						out_video.write(drawed)
						#resized = cv2.resize(frame, (480, 720), interpolation = cv2.INTER_AREA)
						#key_window = self.camera.show(resized)
						#if key_window == 27: break
					if A1==1:
						self.adam.di_output(DigitalOutput(array=[1,0,1,0,0,0]))
						print('Stop recording and app')
						break
					self.prev_A1==A1
				out_video.release()
		self.camera.release()

if __name__ == '__main__':
	application  = RunApplication()
	application.run()

