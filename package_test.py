import sys
import psutil
import dispy
import subprocess32

print('python version: {}.{}.{}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print ('psutil version: {}'.format(psutil.__version__))
print ('dispy version: {}'.format(dispy.__version__))
