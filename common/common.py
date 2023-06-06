import os
for file in os.listdir( os.path.dirname( os.path.realpath(__file__) )):
    if file.endswith(".py") and file != os.path.basename(__file__):
        exec("from {} import *".format(file[:-3]))