import os
import pytz
from pathlib import Path
from datetime import datetime
from config import DIRECTORY_LOGGER

ist = pytz.timezone('Asia/Jakarta')

def datetime_format():
    '''
    Extract daterime now to get year month day hour minute second and microsecond now
    '''
    datetime_now    = datetime.now(ist)
    year            = str(datetime_now.year)
    month           = '0'+str(datetime_now.month) if len(str(datetime_now.month)) == 1 else str(datetime_now.month)
    day             = '0'+str(datetime_now.day) if len(str(datetime_now.day)) == 1 else str(datetime_now.day)
    hour            = '0'+str(datetime_now.hour) if len(str(datetime_now.hour)) == 1 else str(datetime_now.hour)
    minute          = '0'+str(datetime_now.minute) if len(str(datetime_now.minute)) == 1 else str(datetime_now.minute)
    second          = '0'+str(datetime_now.second) if len(str(datetime_now.second)) == 1 else str(datetime_now.second)
    microsecond     = '0'+str(datetime_now.microsecond) if len(str(datetime_now.microsecond)) == 1 else str(datetime_now.microsecond)
    return year, month, day, hour, minute, second, microsecond

def get_path_log():
    '''
    Set path log in path logging/yaer/month/day/log_name.log
    '''
    year, month, day, hour, minute, _, _ = datetime_format()
    path_name = f'{DIRECTORY_LOGGER}/{year}/{month}/{day}'
    Path(path_name).mkdir(parents=True, exist_ok=True)
    log_filename = f'logging_{hour}, {day}-{month}-{year}.log'
    log_file_full_name = os.path.join(path_name, log_filename)
    return log_file_full_name

def asctime():
    '''
    Get asctime for message log
    '''
    year, month, day, hour, minute, second, microsecond = datetime_format()
    return f'{year}-{month}-{day} {hour}:{minute}:{second},{str(microsecond)[:3]}'

class logging:
    '''
    Add class method for level log : info error and debug
    '''
    @classmethod
    def info(self, msg):
        self.__write_log(self, msg, level='INFO')
    @classmethod    
    def error(self, msg):
        self.__write_log(self, msg, level='ERROR')
    @classmethod
    def debug(self, msg):
        self.__write_log(self, msg, level='DEBUG')

    def __write_log(self, message, level):
        '''
        Write text log in path log
        '''
        path_log = get_path_log()
        log_file = open(path_log, 'a+')
        text = f'{asctime()} | {level} : {message}'
        log_file.write(f'{text} \n')
        print(text)
        log_file.close()