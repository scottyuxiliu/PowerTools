import os
import sys

# import kysy modules
load_dir = os.path.abspath('C:/bin/amd/kysy/Python')
sys.path.append(load_dir)
print (sys.path)

from util import Util
from sysexam import Sysexam

connect_type = 'yaap'
ip = '10.1.36.145'
username = 'SMU'
password = 'SMU'

ut = Util(connect_type, ip, username, password)

# Example 1: read register multiple times
def read_screen_refresh_rate():

    reg_path = "PPR::OPTC::OTG::socket0::die0::OTG_V_TOTAL_MIN"
    print (ut.read_register(reg_path, 'hex', True, 20, 1))

    return 0

# Example 2: Sysexam
def sysexam():
    sysexam_verify_xml_path = 'C:/Users/powerhost/pycharmprojects/PowerTools/static/sysexam/raven_verify.xml'
    verify_results_csv_path = 'C:/Users/powerhost/Documents/raven_verify_results_mandolindap.csv'
    sysex = Sysexam(ut)
    sysex.start_sysexam_on_host(sysexam_verify_xml_path, verify_results_csv_path)

sysexam()
