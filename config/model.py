import os

#========================== DIRECTORY =====================================
ROOT 					= os.path.normpath(os.path.dirname(__file__))

DIRECTORY_MODEL         = os.path.expanduser('~/.Halotec/Models')

DIRECTORY_LOGGER        = os.path.expanduser('~/.Halotec/Loggers')

#============================ MODELS ======================================
DETECTION_MODEL = {
	'tires_detection' : {
		'filename'  : 'tires_detection_v1_3.pt',
		'url'       : 'https://www.dropbox.com/s/yhja2nfsopkm52n/tires_detection_v1_3.pt?dl=1',
		'file_size' : 14753191
	}
}

#============================ CLASESS ======================================
CLASSES_DETECTION   = ['tires']
CLASSES_FILTERED    = ['tires']
