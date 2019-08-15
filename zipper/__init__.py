import os
import sys
import logging
import zipfile

def _zipdir(path, ziph, name, logger, ignore = "zip"):
	#Copied and modified for personal use from https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
	logger.warn("Folder detected : "+path)
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.find(ignore) != -1 and len(ignore) > 0:
				logger.warn("Ignored : "+os.path.join(root, f))
			else:
				if f.find(name) != -1:
					logger.warn("Preventing recursion")
				else:
					logger.warn("Writing : "+os.path.join(root, f))
					ziph.write(os.path.join(root, f))
	return
	
def zipper(path, name = "zipper_temp.zip", ignore="zip", logging_level = logging.ERROR, format = '%(name)s %(threadName)s %(asctime)s %(message)s', logfile = sys.stdout):
	logger = logging.Logger(name = "Zipper")
	logger.setLevel(logging_level)
	handler = logging.StreamHandler(logfile)
	handler.setFormatter(logging.Formatter(format))
	logger.addHandler(handler)
	
	#print(logging.CRITICAL)
	if os.path.exists(path):
		zipf = zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED)
		if os.path.isdir(path):
			_zipdir(path, zipf, name, logger, ignore = ignore)
		elif os.path.isfile(path):
			zipf.write(path)
		zipf.close()
		logger.warn("Created : {}".format(name))
		#os.remove("..zip")
		return name
	else:
		return None
	
def unzipper(filename, path ="./", logging_level = logging.ERROR, format = '%(name)s %(threadName)s %(asctime)s %(message)s', logfile = sys.stdout):
	logger = logging.Logger(name="Unzipper")
	logger.setLevel(logging_level)
	handler = logging.StreamHandler(logfile)
	handler.setFormatter(logging.Formatter(format))
	logger.addHandler(handler)
	
	zipf = zipfile.ZipFile(filename, "r", zipfile.ZIP_DEFLATED)
	zipf.extractall(path=path)
	
	logger.warn('Created : {}'.format(path))
	
if __name__ == "__main__":
	zipper("../", ignore="", logging_level = logging.DEBUG, logfile = open("logfile.txt","w+"))
	#unzipper("zipper_temp.zip")