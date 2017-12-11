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
    print (ut.read_register(reg_path, 'hex', True, 20, 1))

    return 0

# Example 2: read multiple registers from xml file and dump results into csv file
def read_fmt_bit_depth_control(self):
    data = []
    start_time = time.time()

    for i in range(1500):
        data.append({'time (s)': time.time()-start_time,
                     'FMT_BIT_DEPTH_CONTROL (FMT0)': self.read_register("PPR::OPP::FMT::socket0::die0::FMT_BIT_DEPTH_CONTROL"),
                     'FMT_BIT_DEPTH_CONTROL (FMT1)': self.read_register("PPR::OPP::FMT::socket0::die0::FMT_BIT_DEPTH_CONTROL_dce_dc_opp_addrmap_fmt1_dispdec_FMT_BIT_DEPTH_CONTROL"),
                     'FMT_BIT_DEPTH_CONTROL (FMT2)': self.read_register("PPR::OPP::FMT::socket0::die0::FMT_BIT_DEPTH_CONTROL_dce_dc_opp_addrmap_fmt2_dispdec_FMT_BIT_DEPTH_CONTROL"),
                     'FMT_BIT_DEPTH_CONTROL (FMT3)': self.read_register("PPR::OPP::FMT::socket0::die0::FMT_BIT_DEPTH_CONTROL_dce_dc_opp_addrmap_fmt3_dispdec_FMT_BIT_DEPTH_CONTROL"),
                     'FMT_BIT_DEPTH_CONTROL (FMT4)': self.read_register("PPR::OPP::FMT::socket0::die0::FMT_BIT_DEPTH_CONTROL_dce_dc_opp_addrmap_fmt4_dispdec_FMT_BIT_DEPTH_CONTROL"),
                     'FMT_BIT_DEPTH_CONTROL (FMT5)': self.read_register("PPR::OPP::FMT::socket0::die0::FMT_BIT_DEPTH_CONTROL_dce_dc_opp_addrmap_fmt5_dispdec_FMT_BIT_DEPTH_CONTROL")})
        print(data[-1])
        time.sleep(2)
    df = pandas.DataFrame(data)
    print (df)
    df.to_csv('C:/Users/jaoliu/Documents/FMT_BIT_DEPTH_CONTROL_0.csv')

    return 0
