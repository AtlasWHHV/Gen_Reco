import sys
import dask
import dask.distributed
import paramiko
import bokeh
import subprocess32

print('python version: {}.{}.{}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print('dask version: {}'.format(dask.__version__))
print('bokeh version: {}'.format(bokeh.__version__))
print('paramiko version: {}'.format(paramiko.__version__))
