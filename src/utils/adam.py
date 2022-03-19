from config import IP, USERNAME, PASSWORD
from adam_io import Adam6050D

class Adam6050Input:
    def __init__(self):
        self.adam           = Adam6050D(IP, USERNAME, PASSWORD)
        
    def di_input(self, di=None):
        '''
        digital output adam,
        and convert digital output to bolean (True/False)
        Args:
            di = Optional -> 0, 1,2,3,4,5,6
        return:
            output = True/False
            
        '''
        dig_in = self.adam.input(0)
        if dig_in[di] == 0: return False
        else: return True

    def di_inputs(self):
        '''
        digital input adam,
        and convert digital input to bolean (True/False)
        
        return:
            output = List[True/False]
        '''
        dig_in = self.adam.input()
        output = [False if i[1]==0 else True for i in dig_in]
        return output