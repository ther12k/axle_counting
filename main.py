import cv2
import time

from src import MainProcess
from src.utils.camera import Camera
from src.utils import Adam6050Input

from src.utils import logging


class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=2, camera_pipeline=False)
		self.camera_run  	= self.camera.run()
		self.adam_input		= Adam6050Input()
		self.app         	= MainProcess()
		self.prev_input		= list()
		self.skip_frame  	= False

	
	def __write_video(self, filename):
		size = (int(self.camera_run.get(3)), int(self.camera_run.get(4)))
		return cv2.VideoWriter(f'{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 10, size)

	def __trigger_camera(self):
		input_list = self.adam_input.di_inputs()
		if not self.prev_input == input_list:
			if not self.prev_input[4] and input_list:
				trigger = True
			self.prev_input = input_list
		else: trigger = True
		return trigger
		 
	def run(self):
		
		start_time 	= time.time()
		timestamp	= int(start_time)
  
		logging.info(f'======== Axle Counting Started ========')
		logging.info(f'Id : {timestamp}')

		# Define Write Video
		#out_video =  self.__write_video(timestamp)

		while True:
			#if self.__trigger_camera():
			ret, frame = self.camera_run.read()
			if not ret:
				logging.error(f'Message : Error reading frame')
				self.camera.release(ret=False)
				self.capture = self.camera.run()
				time.sleep(1)
			else:
				if not self.skip_frame:
					drawed = self.app.main(frame)
						#out_video.write(drawed)
					self.skip_frame = True
				else: self.skip_frame = False; continue
			
				key_window = self.camera.show(drawed)
				if key_window == 27: break

		self.out.release()
		self.camera.release()

if __name__ == '__main__':
	aplication  = RunApplication()
	aplication.run()
