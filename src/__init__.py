import os
from urllib import response
import cv2
import time
import requests

from datetime import datetime
from pathlib import Path
from itertools import chain
from src.app import TiresDetection
from motpy import Detection, MultiObjectTracker
from config import ID_DEVICE, GATE, IP_API, END_POINT
from .utils import logging, draw_rectangle, datetime_format, sending_file

class MainProcess:
	'''
		Main process seal detection
	'''
	def __init__(self):
		self.config_tracking	= { 'order_pos': 1, 'dim_pos': 2,
									'order_size': 0, 'dim_size': 2,
									'q_var_pos': 1000.,
									'r_var_pos': 0.15 }
		self.tires_detection 	= TiresDetection('tires_detection')
		self.tracker_v3			= MultiObjectTracker(dt=0.1)
		self.tracked			= list()
		self.id					= list()
		self.count				= 1

	def __detection(self, image, size, threshold):
		'''
			Detection object
			Args:
				image(np.array) : image for detection
				size(int)       : size image detection
				threshold(float): min confidence
			Return:
				result(dict): {
				casess:[{
					confidence(float): confidence,
					bbox(list) : [x_min, y_min, x_max, y_max]
				}]
			}
		'''
		results = self.tires_detection.\
				detection(image=image, image_size=size)
		result  = self.tires_detection.\
				extract_result(results=results, min_confidence=threshold)
		return result
	
	def __save_and_sending_file(self, file, id_file):
		'''
			Send image to server
			Args:
				file_path(str): path of image
			Return:
				
		'''
		# Save File
		year, month, day, hour, _, _,_ = datetime_format()
		save_path = f'results/{year}/{month}/{day}/{hour}'
		Path(save_path).mkdir(parents=True, exist_ok=True)
		
		file_name   = f'{id_file}.jpg'
		path_image  = f'{save_path}/{file_name}'
		cv2.imwrite(f'{path_image}', file)
		
		# Send file to FTP server
		server_path = f'{GATE}/{ID_DEVICE}/{year}-{month}-{day}_{hour}'
		sender = sending_file(file_name=file_name, server_path=server_path)
		if sender:
			os.remove(path_image)
			
		return server_path
	
	@staticmethod
	def __send_api(server_path, start_time, end_time):
		
		#send json to API
		result_json = {
			'gateId'    : GATE,
			'deviceId'  : ID_DEVICE,
			'result'    : 0,
			'box'       : 
				{
				'x_min': 10,
				'y_min': 11,
				'x_max': 12,
				'y_max': 13
			},
			'filePath'  : server_path,
			'startTime' : datetime.fromtimestamp(start_time),
			'endTime'   : datetime.fromtimestamp(end_time),
			'delayInSeconds' : 2
			
		}
		response = requests.post(url = f'{IP_API}/{END_POINT}', data = result_json)
		print(response)
		try:
			if response.status_code() == 200:
				logging.info(f'Send API success')
				return True
		except:
			logging.error('Cannot send data to API')
			return False
		
	def main(self, image, id=None):
		image_ori = image.copy()
		if not id: id = int(time.time())

		# Detection tires
		result = self.__detection(image, size=360, threshold=0.68)
		if not result: return image_ori

		# Extract result to list
		result_list = [[[x['bbox'], key,  x['confidence']] for x in value]\
					for key, value in result.items()]
		result_list = list(chain(*result_list))

		# Tracking Object
		for idx, val in enumerate(result_list):
			self.tracker_v3.step(detections=[Detection(box=val[0])])
			tracks = self.tracker_v3.active_tracks()
			tracked_a, have_id = [i for i,_ in self.tracked], [j for _,j in self.tracked]
			for track in tracks:
				x_min, y_min, x_max, y_max = list(map(int, track.box))
				if track.id not in tracked_a:
					self.tracked.append([track.id, self.count])
					new_val 	= [[x_min, y_min, x_max, y_max], val[1], val[2], self.count]
					self.count += 1
					
					image_ori = draw_rectangle(image_ori, new_val, resize=100)
				else:
					idx 		= tracked_a.index(track.id)
					id_count 	= have_id[idx]
					new_val 	= [[x_min, y_min, x_max, y_max], val[1], val[2], id_count]
					
					image_ori = draw_rectangle(image_ori, new_val, resize=100)
     
		# # Save and sending file FTP
		# try: server_path = self.__save_and_sending_file(image_drawed, id)
		# except: pass
		# # send data to API
		# try: self.__send_api(server_path, start_time=id, end_time=id)
		# except: pass
		return image_ori