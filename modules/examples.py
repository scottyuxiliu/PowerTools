import os
import sys

# import kysy modules
load_dir = os.path.abspath('C:/Applications/AMD/Kysy/Python')
sys.path.append(load_dir)
print (sys.path)

from util import Util

connect_type = 'yaap'
ip = '10.1.37.106' # jason system
username = 'SMU'
password = 'SMU'

# ip = '10.1.36.145' # efe system
# username = 'smu'
# password = 'smu'

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

# Example 3: Sysexam
def start_sysexam_on_host(sysexam_verify_xml_path, verify_results_csv_path):
    xml_regs_df = ut.xml_to_dataframe(sysexam_verify_xml_path, True, True)
    xml_regs_df = ut.read_register_fields_in_dataframe(xml_regs_df, 'int', False, 200, 20, False) # update bitfield values for each xml_reg
    # print(xml_regs_df)
    # xml_regs_df = xml_regs_df[['status0','path','bitfield','recommend','value0']]
    xml_regs_df.to_csv(verify_results_csv_path)
    return 0

# Example 1: read register multiple times
# read_screen_refresh_rate()
# Example 2: read multiple registers from xml file and dump results into csv file
# read_fmt_bit_depth_control()
# Example 3: Sysexam
start_sysexam_on_host("C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/sysexam/sysexam_registers_rv.xml",
                      "C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/sysexam/rvam4_b0dvt_w10rs3_wmr7c28n_1740rc26_sysexam_4.csv")
# Example 4: Enter/Exit PDM mode
# ut.enter_pdm_mode(True)
# Example 5: Memory Access
# ut.read_memory()