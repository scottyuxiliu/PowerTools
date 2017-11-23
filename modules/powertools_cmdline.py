# TODO: stutter efficiency log_with_pdm_mode
# TODO: util.xml_to_dataframe value as number
# TODO: read_register_fields_in_dataframe check recommend==value

"""
Copyright 2012-2016 ADVANCED MICRO DEVICES, INC. All Rights Reserved.

This software and any related documentation (the "Materials") are the
confidential proprietary information of AMD. Unless otherwise provided
in a software agreement specifically licensing the Materials, the Materials
are provided in confidence and may not be distributed, modified, or
reproduced in whole or in part by any means.

LIMITATION OF LIABILITY: THE MATERIALS ARE PROVIDED "AS IS" WITHOUT ANY
EXPRESS OR IMPLIED WARRANTY OF ANY KIND, INCLUDING BUT NOT LIMITED TO
WARRANTIES OF MERCHANTABILITY, NONINFRINGEMENT, TITLE, FITNESS FOR ANY
PARTICULAR PURPOSE, OR WARRANTIES ARISING FORM CONDUCT, COURSE OF DEALING,
OR USAGE OF TRADE.  IN NO EVENT SHALL AMD OR ITS LICENSORS BE LIABLE FOR
ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF
PROFITS, BUSINESS INTERRUPTION, OR LOSS OF INFORMATION) ARISING OUT OF THE
USE OF OR INABILITY TO USE THE MATERIALS, EVEN IF AMD HAS BEEN ADVISED OF
THE POSSIBILITY OF SUCH DAMAGES.  BECAUSE SOME JURISDICTIONS PROHIBIT THE
EXCLUSION OR LIMITATION OF LIABILITY FOR CONSEQUENTIAL OR INCIDENTAL DAMAGES,
THE ABOVE LIMITATION MAY NOT APPLY TO YOU.

AMD does not assume any responsibility for any errors which may appear in the
Materials nor any responsibility to support or update the Materials.  AMD
retains the right to modify the Materials at any time, without notice,
and is not obligated to provide such modified Materials to you.

NO SUPPORT OBLIGATION: AMD is not obligated to furnish, support, or make any
further information, software, technical information, know-how, or show-how
available to you.

U.S. GOVERNMENT RESTRICTED RIGHTS: The Materials are provided with
"RESTRICTED RIGHTS." Use, duplication, or disclosure by the Government
is subject to the restrictions as set forth in FAR 52.227-14 and DFAR
252.227-7013, et seq., or its successor.  Use of the Materials by the
Government constitutes acknowledgement of AMD's proprietary rights in them.

"""

"""
add C:\Program Files (x86)\AMD\Kysy\Python to sys.path
"""

import click
import os
# import built in modules
import sys

import matplotlib.pyplot

# import kysy modules
# print(os.path.abspath('C:\Program Files (x86)\AMD\Kysy\Python'));
load_dir = os.path.abspath('C:\Program Files (x86)\AMD\Kysy\Python')
sys.path.append(load_dir)

from util import Util
from stutter_efficiency import StutterEfficiency
from sysexam import Sysexam


@click.command()
@click.option('--ip', prompt='Wombat IP', help='wombat IP')
@click.option('--username', prompt=True, help='username used in HDT')
@click.option('--password', prompt=True, help='password used in HDT')
@click.option('--groupread', is_flag=True, help='read a group of registers listed in xml file')
@click.option('--groupwrite', is_flag=True, help='write a group of registers listed in xml file')
@click.option('--stutter', is_flag=True, help='launch stutter efficiency logging')
@click.option('--sysexam', is_flag=True, help='launch sysexam')
def powertools_cmdline(ip, username, password, groupread, groupwrite, stutter, sysexam):

    connect_type = 'yaap'
    ip = str(ip)
    username = str(username)
    password = str(password)

    ut = Util(connect_type, ip, username, password)

    if groupread is True:
        if click.confirm("xml file path is C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/raven_verify.xml?"):
            xml_file_path = 'C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/raven_verify.xml'
        else:
            xml_file_path = click.prompt('Please enter results path', type=str)

        if click.confirm("results path is C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/groupread_results.csv?"):
            results_csv_path = 'C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/groupread_results.csv'
        else:
            results_csv_path = click.prompt('Please enter results path', type=str)

        ut.read_register_fields_in_xml_file(xml_file_path, results_csv_path, 'hex', True, True)

    if groupwrite is True:
        if click.confirm("xml file path is ?"):
            xml_file_path = ''
        else:
            xml_file_path = click.prompt('Please enter results path', type=str)

        ut.write_register_fields_in_xml_file(xml_file_path, True)

    if stutter is True:
        se = StutterEfficiency(ut)
        if click.confirm("verify results path is C:/Users/jaoliu/Documents/stutter_efficiency_0.csv?"):
            stutter_efficiency_result_csv_path = 'C:/Users/jaoliu/Documents/stutter_efficiency_0.csv'
        else:
            stutter_efficiency_result_csv_path = click.prompt('Please enter results path', type=str)

        se.read_stutter(60, 1, True, False, stutter_efficiency_result_csv_path)

    if sysexam is True:
        if click.confirm("verify xml path is C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/raven_verify.xml?"):
            sysexam_verify_xml_path = 'C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/raven_verify.xml'
        else:
            sysexam_verify_xml_path = click.prompt('Please enter verify xml path', type=str)

        if click.confirm("results path is C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/raven_verify_results_mandolindap.csv?"):
            verify_results_csv_path = 'C:/Users/jaoliu/Downloads/tools/sysexam/sysexam_RV/raven_verify_results_mandolindap.csv'
        else:
            verify_results_csv_path = click.prompt('Please enter results path', type=str)

        sysex = Sysexam(ut)
        sysex.start_sysexam_on_host(sysexam_verify_xml_path, verify_results_csv_path)


    
    raw_power = 'C:/Users/jaoliu/Downloads/HP Rockets B31A05_HP1025beta150827a406E_mm14_Asystem_r2_analysis.csv'
    #raw_residency = 'C:\\Users\\jaoliu\\Documents\\br_rs2_mm14_panel_power_analysis_data.csv'

    #df = ldt.loadcsv_mm14_1_5(raw_power)
    #plt.stackedline(df.index,df[['Panel_logic_P','Panel_backlight_P']],'Panel Power (W)')
    #plt.stackedline(df.index,df[['902 <Total System Power_P> (WAT)','onenote','chrome','winzip','idle_0','word','powerpoint','acrobat','idle_1','outlook','excel','idle_2']],'Total System Power (W)')

    # ut.read_fmt_bit_depth_control()


if __name__ == '__main__':
    powertools_cmdline()
    matplotlib.pyplot.show()