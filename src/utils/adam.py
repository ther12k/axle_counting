from config import IP, USERNAME, PASSWORD
from adam_io import Adam6050D, DigitalOutput

class Adam6050DInput:
	def __init__(self):
		self.adam           = Adam6050D(IP, USERNAME, PASSWORD)
		self.initial_array  = [0,0,0,0,0,0]
		self.dig_out        = DigitalOutput(array=self.initial_array)

	def di_output(self, initial_array):
		self.adam.output(initial_array)

	def di_input(self, di=None):
		'''
		digital output adam,
		and convert digital output to bolean (True/False)
		Args:
			di = Optional -> 1,2,3,4,5,6
		return:
			output = True/False
			
		'''
		dig_in = self.adam.input(0)
		if dig_in[di-1] == 0: return False
		else: return True

	def di_inputs(self):
		'''
		digital output adam,
		and convert digital output to bolean (True/False)
		Args:
			di = Optional -> 1,2,3,4,5,6
		return:
			output = List[True/False]
		'''
		dig_in = self.adam.input()
		
		#print(f'A1={dig_in[7]} | A2={dig_in[6]} | B1={dig_in[5]} | B2={dig_in[4]}')
		return [
			('A1',dig_in[7]),
			('A2',dig_in[6]),
			('B1',dig_in[5]),
			('B2',dig_in[4])
		]
