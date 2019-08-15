# Zipper utility

Provides 2 loggable methods:
1. zipper(path, name = "zipper_temp.zip", ignore="zip", logging_level = logging.ERROR, format = '%(name)s %(threadName)s %(asctime)s %(message)s', logfile = sys.stdout)
2. unzipper(filename, path ="./", logging_level = logging.ERROR, format = '%(name)s %(threadName)s %(asctime)s %(message)s', logfile = sys.stdout)

Pretty self explnatory. Use it as you like.
Thread not tested yet. But is expected to be thread safe.