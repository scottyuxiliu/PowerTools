import os
import sys

# import kysy modules
load_dir = os.path.abspath('C:/Applications/AMD/Kysy/Python')
sys.path.append(load_dir)
print (sys.path)

from util import Util

connect_type = 'yaap'
ip = '10.1.36.145'
username = 'smu'
password = 'smu'

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
    xml_regs_df = ut.read_register_fields_in_dataframe(xml_regs_df, 'hex', True, 1, 1, True) # update bitfield values for each xml_reg
    print(xml_regs_df)
    # print xml_regs_df.columns.tolist()
    xml_regs_df = xml_regs_df[['status0','path','bitfield','recommend','value0']]

    xml_regs_df.to_csv(verify_results_csv_path)
    return 0


# read_screen_refresh_rate()
# read_fmt_bit_depth_control()
start_sysexam_on_host("C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/sysexam/sysexam_registers_rv.xml",
                      "C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/sysexam/rvfp5_b0dvt_15w_jasonsystem_w10rs3_vmd8944n_1740rc26_sysexam_0.csv")