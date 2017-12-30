import os
import sys

# import kysy modules
load_dir = os.path.abspath('C:/bin/amd/kysy/Python')
sys.path.append(load_dir)
print (sys.path)

from util import Util

connect_type = 'yaap'
ip = '10.1.37.106'
username = 'SMU'
password = 'SMU'

ut = Util(connect_type, ip, username, password)


# Example 1: read register multiple times
def read_screen_refresh_rate():

    reg_path = "PPR::OPTC::OTG::socket0::die0::OTG_V_TOTAL_MIN"
    print (ut.read_register(reg_path, 'hex', True, 10, 1))

    return 0

# Example 2: read multiple registers from xml file and dump results into csv file
def read_fmt_bit_depth_control():
    ut.read_registers_in_xml_file("C:/Users/powerhost/pycharmprojects/PowerTools/static/examples/read_fmt_bit_depth_control.xml",
                                  "C:/Users/powerhost/pycharmprojects/PowerTools/static/examples/read_fmt_bit_depth_control_results.csv",
                                  'hex',
                                  True,
                                  10,
                                  1)
    return 0



# read_screen_refresh_rate()
read_fmt_bit_depth_control()