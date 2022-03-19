# # import cv2
# # from src import MainProcess

# # app = MainProcess()

# # image = cv2.imread('images/1.jpg')
# # app.main(image)
import json
# import time
# import requests
# from config import *

# from datetime import datetime

# def __send_api(server_path, start_time=time.time(), end_time=time.time()):
#         headers = {
#             'accept': '*/*',
#             'Content-Type': 'application/json',
#         }
#         #send json to API
#         result_json = {
#             'gateId'    : '09',
#             'deviceId'  : 'sealdetection09',
#             'result'    : 0,
#             'box'       : 
#                 {
#                 'x_min': 10,
#                 'x_max': 11,
#                 'y_min': 12,
#                 'y_max': 13
#             },
#             'filePath'  : server_path,
#             'startTime' : str(datetime.fromtimestamp(start_time)),
#             'endTime'   : str(datetime.fromtimestamp(end_time)),
#             'delayInSeconds' : 2
            
#         }
#         response = requests.post(url = f'{IP_API}/{END_POINT}', headers=headers, data = result_json)
#         print(response)
#         try:
#             response = requests.post(url = f'{IP_API}/{END_POINT}', data = result_json)
#             if response.status_code() == 200:
#                 print(f'Send API success')
#                 return True
#         except:
#             print('Cannot send data to API')
#             return False
        
# print(__send_api('/test'))

import requests

headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
}

json_data = {
    'gateId': 'gate09',
    'deviceId': '1',
    'result': 2,
    'confidence': 90,
    'box': {
        'x_min': 0,
        'x_max': 0,
        'y_min': 0,
        'y_max': 0,
    },
    'filePath': 'string',
    "startTime": "2022-03-19T08:49:28.315Z",
    "EndTime": "2022-03-19T08:49:28.315Z",
    'delayInSeconds': 9,
}
print(json.dumps(json_data))
response = requests.post('https://3973-114-4-83-199.ngrok.io/api/v1/seal', headers=headers, json=json_data)
print(response.text)