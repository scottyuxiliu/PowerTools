import os
import sys
import matplotlib.pyplot

# import kysy modules
load_dir = os.path.abspath('C:/Applications/AMD/Kysy/Python')
sys.path.append(load_dir)
print (sys.path)

from util import Util
from stutter_efficiency import StutterEfficiency

connect_type = 'yaap'

ip = '10.1.37.106' # jason system
username = 'SMU'
password = 'SMU'

# ip = '10.1.36.145' # efe system
# username = 'smu'
# password = 'smu'

ut = Util(connect_type, ip, username, password)
st = StutterEfficiency(ut)


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

# Example 1: read register multiple times
# read_screen_refresh_rate()

# Example 2: read multiple registers from xml file and dump results into csv file
# read_fmt_bit_depth_control()

# Example 3: Sysexam
ut.read_register_fields_in_xml_file("C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/sysexam/xml/PRPinnacleRidgeAM4/sysexam_registers_pram4_umc.xml",
                                    "C:/Users/powerhost/Documents/AMD/Projects/PRPinnacleRidgeAM4/Data/SystemPwrFeatures/Idle/SysExam/pram4_turpandap_w10rs3_wmp8124n_17.12.2adrenalinedition_stack1.0.0_umc_sysexam_0.csv",
                                    'hex',
                                    True,
                                    15,
                                    3,
                                    True)

# Example 4: Enter/Exit PDM mode
# ut.enter_pdm_mode(True)

# Example 5: Memory Access
# ut.read_memory()

# Example 4: Stutter Efficiency
# st.read_stutter(300, 1, True, True, "C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/stutter_efficiency/rvfp5_b0dvt_w10rs3_tmd1004fa_1740rc26_idlestutter_1.csv")

# Example 5: MM14 Plot
# df = ut.loadcsv_mm14("C:/Users/powerhost/Documents/AMD/Projects/RVRavenRidgeFP5/Data/MandolinDAP/SystemPwrFeatures/R7vsR5/Power/TMD1102_1740RC33_default_MM14_wk61_TSP_R5_run1.csv", 25, 30, 0.5)

# Example 6: Read SMN Buffer
# ut.read_smn_buffer(0x5012C, 8, 4)

# Example 7: Read MP1 Buffer
# ut.read_mp1_buffer(0x8578, 'hex', True)

# Example 8: Read everything
# dictlist = ut.xml_to_dictlist("C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/sysexam/xml/PRPinnacleRidgeAM4/sysexam_test.xml")
# ut.read_all_in_dictlist(dictlist, 'hex', True, 100, 10, False).to_csv("C:/Users/powerhost/Documents/PycharmProjects/PowerTools/static/test/results.csv")

# Example 9: Week of 2018.01.22 Optimized Settings
# ut.write_all_in_xml_file("C:/Users/powerhost/Documents/AMD/Projects/PRPinnacleRidgeAM4/Data/SystemPwrFeatures/WeeklyUpdate/2018.01.22/optimized_settings_weekof_2018.01.22.xml", True)
# ut.read_all_in_xml_file("C:/Users/powerhost/Documents/AMD/Projects/PRPinnacleRidgeAM4/Data/SystemPwrFeatures/WeeklyUpdate/2018.01.22/optimized_settings_weekof_2018.01.22.xml",
#                         "C:/Users/powerhost/Documents/AMD/Projects/PRPinnacleRidgeAM4/Data/SystemPwrFeatures/WeeklyUpdate/2018.01.22/optimized_settings_weekof_2018.01.22_results.csv",
#                         'hex',
#                         True,
#                         50,
#                         10)
