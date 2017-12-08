import os
import sys

# import kysy modules
load_dir = os.path.abspath('C:/bin/amd/kysy/Python')
sys.path.append(load_dir)
print (sys.path)

from util import Util

connect_type = 'yaap'
ip = '10.1.37.106'
username = 'kysy'
password = 'kysy'

ut = Util(connect_type, ip, username, password)

ut.read_memory(0x124c4,8)