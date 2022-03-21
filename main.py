import cv2
import time
from src import MainProcess
from adam_io import DigitalOutput
from src.utils import Adam6050DInput
from src.utils.camera import Camera
from adam_io import DigitalOutput

class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=0)
		self.camera_run  	= self.camera.run()
		self.adam			= Adam6050DInput()
		self.app         	= MainProcess()
		self.prev_A1		= 1
	
	def __write_video(self, filename):
		size = (int(self.camera_run.get(4)), int(self.camera_run.get(3)))
		return cv2.VideoWriter(f'results/{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 20, (1080,1920))

	def run(self):
		while True:
			adam_inputs = self.adam.di_inputs()
			A1, A2 = adam_inputs[0][1], adam_inputs[1][1]
			B1, B2 = adam_inputs[2][1], adam_inputs[3][1]
			# Condition start recording and running app
			if self.prev_A1==1 and A1==0:
			#if A1==0 and A2==1 and B1==1 and B2==1:
				print('Start recording')
				time_now = int(time.time())
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
						drawed = self.app.main(frame)
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

