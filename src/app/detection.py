import os
import sys
import torch
import requests
from tqdm import tqdm
from pathlib import Path

from config import(
	DIRECTORY_MODEL, 
	DETECTION_MODEL,
	CLASSES_DETECTION,
	CLASSES_FILTERED
)

class TiresDetection:
	'''
	Load custom model YoloV5
	for detection tires vehicle
	'''
	def __init__(self, model_name):
		self.model_name = model_name
		self.device     = 'cuda' if torch.cuda.is_available() else 'cpu'
		self.model_path = os.path.join(DIRECTORY_MODEL, DETECTION_MODEL[self.model_name]['filename'])
		self.__check_model()
		self.model      = self.__load_model(self.model_path)
		
	@staticmethod
	def __load_model(model_path):
		try: model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		except: sys.exit('Error load model')
		return model
			
	def __check_model(self):
		'''
		Checking model in model_path
		download model if file not found
		'''
		Path(DIRECTORY_MODEL).mkdir(parents=True, exist_ok=True)
		if not os.path.isfile(self.model_path):
			print(f'Downloading {self.model_name} detection model, please wait.')
			response = requests.get(DETECTION_MODEL[self.model_name]['url'], stream=True)
			
			progress = tqdm(response.iter_content(1024), 
						f'Downloading {DETECTION_MODEL[self.model_name]["filename"]}', 
						total=DETECTION_MODEL[self.model_name]['file_size'], unit='B', 
						unit_scale=True, unit_divisor=1024)
			with open(self.model_path, 'wb') as f:
				for data in progress:
					f.write(data)
					progress.update(len(data))
				print(f'Done downloaded {DETECTION_MODEL[self.model_name]["filename"]} detection model.')
		else:
			print(f'Load {DETECTION_MODEL[self.model_name]["filename"]} detection model.')

	@staticmethod
	def extract_result(results, min_confidence=0.0):
		'''
		Format result([tensor([[151.13147, 407.76913, 245.91382, 454.27802,   0.89075,   0.00000]])])
		Filter min confidence prediction and classes id/name
		Cropped image and get index max value confidence lavel
		Args:
			result(models.common.Detections): result detection YoloV5
			min_confidence(float): minimal confidence detection in range 0-1
		Return:
			result(dict): {
				casess:[{
					confidence(float): confidence,
					bbox(list) : [x_min, y_min, x_max, y_max]
				}]
			}
		'''
		results_format  = results.xyxy
		results_filter =  dict({i:list() for i in CLASSES_FILTERED})
		
		if len(results_format[0]) >= 1:
			for i in range(len(results_format[0])):
				classes_name    = CLASSES_DETECTION[int(results_format[0][i][-1])]
				confidence      = float(results_format[0][i][-2])
				if classes_name in CLASSES_FILTERED and confidence >= min_confidence:
					x_min, y_min = int(results_format[0][i][0]), int(results_format[0][i][1])
					x_max, y_max = int(results_format[0][i][2]), int(results_format[0][i][3])
					
					results_filter[classes_name].append(
						{'confidence': round(confidence,2), 
						'bbox':[x_min, y_min, x_max, y_max]}
					)
		# Delete key if detection null
		for i in CLASSES_FILTERED:results_filter.__delitem__(i) if not results_filter[i] else None

		return results_filter

	def release(self):
		'''
			Empty cache cuda memory
		'''
		del self.model
		torch.cuda.empty_cache()
	
	def detection(self, image, image_size=None):
		'''
		Prediction image object detectionn YoloV5
		Args:
			image(numpy.ndarray) : image/frame
		Return:
			results_prediction(models.common.Detections) : results -> convert to (results.xyxy/resultsxywh)
		'''
		if image_size: results = self.model(image, size=image_size)
		else: results = self.model(image)
		return results
