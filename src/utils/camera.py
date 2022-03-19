import cv2
import time
from config import WIDTH, HEIGH

class Camera:
	def __init__(self, camera_id=0, flip_method=0, camera_pipeline=True):
		self.camera_id 	= camera_id
		if camera_pipeline:
			self.cap = cv2.VideoCapture(self.__gstreamer_pipeline(camera_id=camera_id, flip_method=flip_method), cv2.CAP_GSTREAMER)
		else:
			self.cap = cv2.VideoCapture(camera_id)
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
  
	def run(self):
		while not self.cap.isOpened():
			print("Error opening video stream or file")
			self.cap.release(); time.sleep(1)
			self.__init__(self.camera_id)
		return self.cap

	@staticmethod
	def __gstreamer_pipeline(
		camera_id,
		capture_width=WIDTH,
		capture_height=HEIGH,
		display_width=WIDTH,
		display_height=HEIGH,
		framerate=30,
		flip_method=0,
	):
		return (
			"nvarguscamerasrc sensor-id=%d ! "
			"video/x-raw(memory:NVMM), "
			"width=(int)%d, height=(int)%d, "
			"format=(string)NV12, framerate=(fraction)%d/1 ! "
			"nvvidconv flip-method=%d ! "
			"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
			"videoconvert ! "
			"video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
			% (
				camera_id,
				capture_width,
				capture_height,
				framerate,
				flip_method,
				display_width,
				display_height,
			)
		)
  
	def release(self, ret=True):
		self.cap.release()
		if not ret: self.run()
		cv2.destroyAllWindows()
	
	def show(self,frame, window_name='Frame'):
		cv2.imshow(window_name, frame)
		return cv2.waitKey(30)
