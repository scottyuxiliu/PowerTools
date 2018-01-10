import argparse
import numpy
import math
import pandas
import time
from lxml import etree

import KysyEnvironment
import Kysy


class Util:
    """
    contains util functions:

    read_register
    read_register_field

    read_xml
    read_xml_registers
    read_xml_register_fields
    write_xml_register_fields

    """
    def __init__(self,
                 connect_type=None,
                 ip=None,
                 username=None,
                 password=None):
        """

        :param connect_type:
        :param ip:
        :param username:
        :param password:
        """

        print ("loading util class..."),
        try:
            Kysy.StubPlatform.create
        except RuntimeError as e:
            print("Exception: %s\n" % str(e))

        if connect_type is None:
            parser = argparse.ArgumentParser(
                description='Sample parser of args to support different target access methods')
            parser.add_argument('--yaap', action="store", dest="yaap", help='Wombat IP address')
            parser.add_argument('--hdt', action="store", dest="hdt", help='Wombat IP address (deprecated)')
            parser.add_argument('--sim', nargs='?', const='sim', default='default')

            args = parser.parse_args()

            # Parse out the args and construct a platform instance
            if args.yaap is not None:
                self.wombat = Kysy.Wombat.create(args.yaap)
                self.platform = self.wombat.platform()
                # enter debug mode before the sample test
                # wombat.cpuDebug().requestDebug()
            elif args.hdt is not None:
                self.hdt = Kysy.HDTYaapDevice.create(args.hdt)
                self.platform = self.hdt.platform()
                # Enter debug mode before the sample test
                # hdt.cpuDebug().requestDebug()
            elif args.sim is not None and args.sim == 'sim':
                # We connect to an existing SimNow session. Hence passing in an empty string.
                self.sim = Kysy.SimNowDevice.create('')
                self.platform = self.sim.platform()
                # sim.cpuDebug().requestDebug()
            else:
                # Construct a native platform
                self.platform = Kysy.Platform.create()
        else:
            if connect_type == 'yaap':
                self.wombat = Kysy.Wombat.create(ip, username, password)
                self.platform = self.wombat.platform()
        print ("done")

    """ wombat section """
    def get_wombat_platform(self):
        return self.wombat, self.platform

    """ register access section """

    def enter_pdm_mode(self, verbose=False):
        if self.wombat.cpuDebug().debugEnabled() == 1:
            if verbose is True:
                print ("CPU already in debug mode")
        else:
            for i in range(10):
                if self.wombat.cpuDebug().debugEnabled() == 0:
                    if verbose is True:
                        print ("attempting to enter PDM mode...")
                    self.wombat.cpuDebug().requestDebug()
                    time.sleep(5)
                else:
                    if verbose is True:
                        print ("success")
                    return 0
            raise TypeError('Did you forget to disable CPUOFF?')

    def exit_pdm_mode(self, verbose=False):
        if self.wombat.cpuDebug().debugEnabled() == 0:
            if verbose is True:
                print ("CPU already out of debug mode")
        else:
            while self.wombat.cpuDebug().debugEnabled() == 1:
                if verbose is True:
                    print ("attempting to exit PDM mode..."),
                self.wombat.cpuDebug().exitDebug()
                time.sleep(5)
            if verbose is True:
                print("success")

    def read_memory(self):
        pprCoreTopoIDs = Kysy.PPRCoreTopologyPhysicalIDs(0, 0, 0, 0, 0)
        bytes = Kysy.Bytes(0x4)
        mem = Kysy.PhysicalMemorySpace.mapMemory(self.platform.platformAccess(), pprCoreTopoIDs, 0xFED80E78, bytes, Kysy.MEMORY_DESTINATION_MMIO, Kysy.MEMORY_TYPE_UNCACHEABLE, Kysy.MEMORY_ACCESS_SIZE_64BIT)
        mem.fill(0)
        mem.read()
        return 0

    def read_register(self, register_path, return_type='hex', verbose=False):
        """
        read register
        :param register_path:
        :param return_type: return hex or int
        :param verbose: output all the messages
        :return: value, default to register hex value
        """

        register = self.platform.regByPath(register_path)
        register.read()
        if return_type == 'hex':
            if verbose is True:
                print ("reading {0}...".format(register_path))
            value = hex(register.value()).rstrip('L')
            if verbose is True:
                print("    {0} = {1}".format(register_path, value))
        elif return_type == 'int':
            if verbose is True:
                print ("reading {0}...".format(register_path))
            value = register.value()
            if verbose is True:
                print("    {0} = {1}".format(register_path, value))
        else:
            raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

        return value

    def read_registers(self, register_path, return_type='hex', verbose=False, log_duration=1, log_period=1):
        """
        read register
        :param register_path:
        :param return_type: return hex or int
        :param verbose: output all the messages
        :param log_duration: number of seconds to log
        :param log_period: number of seconds to wait between two reads
        :return: df, default to register hex value
        """
        dictlist = []
        repeat = log_duration / log_period

        for i in range(repeat):
            register = self.platform.regByPath(register_path)
            register.read()
            if return_type == 'hex':
                if verbose is True:
                    print ("reading {0}...".format(register_path))
                value = hex(register.value()).rstrip('L')
                if verbose is True:
                    print("    {0} = {1}".format(register_path, value))
                dictlist.append({"path": register_path, "value": value})
            elif return_type == 'int':
                if verbose is True:
                    print ("reading {0}...".format(register_path))
                value = register.value()
                if verbose is True:
                    print("    {0} = {1}".format(register_path, value))
                dictlist.append({"path": register_path, "value": value})
            else:
                raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

            time.sleep(log_period)

        return pandas.DataFrame(dictlist)

    def read_register_field(self,
                            register_path,
                            register_field_name,
                            return_type='hex',
                            verbose=False,
                            log_duration=1,
                            log_period=1):
        """
        read a single register field
        :param register_path:
        :param register_field_name:
        :param return_type:
        :param verbose: output all the messages
        :param log_duration: number of seconds to log
        :param log_period: number of seconds to wait between two reads
        :return: df
        """
        dictlist = []
        value = 0
        repeat = log_duration / log_period

        for i in range(repeat):
            register = self.platform.regByPath(register_path)
            register.read()
            if return_type == 'hex':
                if verbose is True:
                    print ("reading {0}[{1}]...".format(register_path, register_field_name))
                value = hex(register.field(register_field_name).value()).rstrip('L')
                if verbose is True:
                    print("    {0}[{1}] = {2}".format(register_path, register_field_name, value))
                dictlist.append({"path": register_path, "field": register_field_name, "value": value})
            elif return_type == 'int':
                if verbose is True:
                    print ("reading {0}[{1}]...".format(register_path, register_field_name))
                value = register.field(register_field_name).value()
                if verbose is True:
                    print("    {0}[{1}] = {2}".format(register_path, register_field_name, value))
                dictlist.append({"path": register_path, "field": register_field_name, "value": value})
            else:
                raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

            time.sleep(log_period)

        return pandas.DataFrame(dictlist)

    def read_registers_in_dataframe(self,
                                    registers_dataframe,
                                    return_type='hex',
                                    verbose=False,
                                    log_duration=1,
                                    log_period=1):
        """

        :param registers_dataframe: must have path
        :param return_type:
        :param verbose: print out each register read
        :param log_duration: number of seconds to log
        :param log_period: number of seconds to wait between two reads
        :return: dataframe
        """
        regs_dictlist = registers_dataframe.to_dict('records')
        repeat = log_duration / log_period

        for i in range(repeat):
            if return_type == 'hex':
                for reg_dict in regs_dictlist:
                    if verbose is True:
                        print ("reading {0}...".format(reg_dict['path']))

                    register = self.platform.regByPath(reg_dict['path'])
                    register.read()
                    reg_dict['value'+str(i)] = hex(register.value()).rstrip('L')

                    if verbose is True:
                        print ("    {0} = {1}".format(reg_dict['path'], reg_dict['value'+str(i)]))
            elif return_type == 'int':
                for reg_dict in regs_dictlist:
                    if verbose is True:
                        print ("reading {0}...".format(reg_dict['path']))

                    register = self.platform.regByPath(reg_dict['path'])
                    register.read()
                    reg_dict['value'+str(i)] = register.value()

                    if verbose is True:
                        print ("    {0} = {1}".format(reg_dict['path'], reg_dict['value'+str(i)]))
            else:
                raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

        return pandas.DataFrame(regs_dictlist)

    def read_register_fields_in_dataframe(self,
                                          registers_dataframe,
                                          return_type='hex',
                                          verbose=False,
                                          log_duration=1,
                                          log_period=1,
                                          status_check=True):
        """

        :param registers_dataframe: must have path and bitfield; if status_check is true, recommend must be present
        :param return_type:
        :param verbose: print out each register read
        :param log_duration: number of seconds to log
        :param log_period: number of seconds to wait between two reads
        :param status_check: check if value == recommend
        :return: df
        """
        regs_dictlist = registers_dataframe.to_dict('records')
        repeat = log_duration / log_period

        # if checking recommend == value, recommend field must be present in the dataframe, otherwise skip status check
        if status_check is True:
            if any('recommend' in reg_dict for reg_dict in regs_dictlist) is False:
                print ('there is no recommend column in the dataframe passed in')
                status_check = False

        for i in range(repeat):
            if return_type == 'hex':
                for reg_dict in regs_dictlist:
                    if verbose is True:
                        print ("reading {0}[{1}]...".format(reg_dict['path'], reg_dict['bitfield'])),

                    register = self.platform.regByPath(reg_dict['path'])
                    register.read()

                    if verbose is True:
                        print ("done")

                    reg_dict['value'+str(i)] = hex(register.field(reg_dict['bitfield']).value()).rstrip('L')

                    if verbose is True:
                        print ("    {0}[{1}] = {2}".format(reg_dict['path'],
                                                           reg_dict['bitfield'],
                                                           reg_dict['value'+str(i)]))
                    # check if recommend == value
                    if status_check is True:
                        if reg_dict['recommend'] == reg_dict['value'+str(i)]: reg_dict.update({'status'+str(i): ''})
                        else: reg_dict.update({'status'+str(i): 'BAD'})

            elif return_type == 'int':
                for reg_dict in regs_dictlist:
                    if verbose is True:
                        print ("reading {0}[{1}]...".format(reg_dict['path'], reg_dict['bitfield'])),
                    register = self.platform.regByPath(reg_dict['path'])
                    register.read()
                    if verbose is True:
                        print ("done")
                    reg_dict['value'+str(i)] = register.field(reg_dict['bitfield']).value()
                    if verbose is True: print ("    {0}[{1}] = {2}".format(reg_dict['path'],
                                                                           reg_dict['bitfield'],
                                                                           reg_dict['value'+str(i)]))

                    if status_check is True:
                        reg_dict['recommend'] = int(reg_dict['recommend'], 16) # convert hex to int
                        if reg_dict['recommend'] == reg_dict['value'+str(i)]: reg_dict.update({'status'+(i): ''})
                        else: reg_dict.update({'status'+str(i): 'BAD'})
            else:
                raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

        return pandas.DataFrame(regs_dictlist)

    def read_registers_in_xml_file(self,
                                   xml_file_path,
                                   results_csv_path=None,
                                   return_type='hex',
                                   verbose=False,
                                   log_duration=1,
                                   log_period=1):
        """

        :param xml_file_path:
        :param results_csv_path:
        :param return_type:
        :param verbose:
        :param log_duration: number of seconds to log
        :param log_period: number of seconds to wait between two reads
        :return:
        """

        df = self.xml_to_dataframe(xml_file_path, False, False)
        df = self.read_registers_in_dataframe(df, return_type, verbose, log_duration, log_period)
        if verbose is True:
            print(df)
        if results_csv_path is not None:
            return df.to_csv(results_csv_path)

    def read_register_fields_in_xml_file(self,
                                         xml_file_path,
                                         results_csv_path=None,
                                         return_type='hex',
                                         verbose=False,
                                         log_duration=1,
                                         log_period=1,
                                         status_check=False):
        """

        :param xml_file_path:
        :param results_csv_path:
        :param return_type:
        :param verbose:
        :param log_duration: number of seconds to log
        :param log_period: number of seconds to wait between two reads
        :param status_check:
        :return:
        """

        df = self.xml_to_dataframe(xml_file_path, True, status_check)
        df = self.read_register_fields_in_dataframe(df, return_type, verbose, log_duration, log_period, status_check)
        if verbose is True:
            print(df)
        if results_csv_path is not None:
            return df.to_csv(results_csv_path)

    def write_register(self, register_path, register_value, verbose=False):
        """
        write a value to a single register
        :param register_path:
        :param register_value:
        :param verbose:
        :return:
        """
        register = self.platform.regByPath(register_path)
        if verbose is True: print ("writing {0} to {1}...".format(hex(register_value).rstrip('L'), register_path)),
        register.value(register_value)
        register.write()

        if verbose is True: # read back when verbose is true
            print ("done")
            time.sleep(2)
            register.read()
            print("    {0} = {1}".format(register_path, hex(register.value()).rstrip('L')))

    def write_register_field(self, register_path, register_field_name, register_field_value, verbose=False):


        """
        write a single register field
        :param register_path:
        :param register_field_name:
        :param register_field_value:
        :param verbose:
        :return:
        """
        register = self.platform.regByPath(register_path)

        if verbose is True: print ("writing {0} to {1}...".format(hex(register_field_value).rstrip('L'),
                                                                  register_field_name)),
        register.field(register_field_name).value(register_field_value)
        register.write()

        if verbose is True: # read back when verbose is true
            print ("done")
            time.sleep(2)
            register.read()
            print("    {0}[{1}] = {2}".format(register_path,
                                                              register_field_name,
                                                              hex(register.field(register_field_name).value()).rstrip('L')))

    def write_registers_in_dataframe(self, registers_dataframe, verbose=False):
        """
        the registers_dataframe must contain path and recommend fields
        :param registers_dataframe: recommend field must be number format
        :return:
        """
        regs_dictlist = registers_dataframe.to_dict('records')
        for reg_dict in regs_dictlist:
            if verbose is True: print ("writing {0} to {1}...".format(hex(reg_dict['recommend']).rstrip('L'),
                                                                      reg_dict['path'])),

            register = self.platform.regByPath(reg_dict['path'])
            register.value(reg_dict['recommend'])
            register.write()

            if verbose is True:
                print ("done")
                time.sleep(2)
                register.read()
                print("    {0} = {1}".format(reg_dict['path'],
                                             hex(register.value()).rstrip('L')))

    def write_register_fields_in_dataframe(self, registers_dataframe, verbose=False):
        """
        the registers_dataframe must contain path, bitfield and recommend fields
        :param registers_dataframe:
        :param return_type:
        :param verbose: print out each register read
        :return:
        """
        regs_dictlist = registers_dataframe.to_dict('records')
        for reg_dict in regs_dictlist:
            if verbose is True: print ("writing {0} to {1}...".format(hex(reg_dict['bitfield']).rstrip('L'),
                                                                      reg_dict['bitfield'])),

            register = self.platform.regByPath(reg_dict['path'])
            register.field(reg_dict['bitfield']).value(reg_dict['recommend'])
            register.write()

            if verbose is True:
                print ("done")
                time.sleep(2)
                register.read()
                print("    {0}[{1}] = {2}".format(reg_dict['path'],
                                                  reg_dict['bitfield'],
                                                  hex(register.field(reg_dict['bitfield']).value()).rstrip('L')))

    def write_register_fields_in_xml_file(self, xml_file_path, verbose=False):
        """

        :param xml_file_path:
        :param verbose:
        :return:
        """

        df = self.xml_to_dataframe(xml_file_path)
        self.write_register_fields_in_dataframe(df, verbose)

    """ data loading section """
    def xml_to_dataframe(self, xml_file_path, bitfield_present=False, recommend_present=False):
        """
        read the xml file of registers and convert them to a dataframe

        :param xml_file_path:
        :param bitfield_present: if the xml file has bitfield attribute
        :param recommend_present: if the xml file has recommend attribute
        :return: df
        """
        xml_file = etree.parse(xml_file_path)
        xml_regs = []

        if bitfield_present is False and recommend_present is False:
            for xml_reg in xml_file.findall('reg'):
                xml_regs.append({'path': xml_reg.get('path')})
        elif bitfield_present is True and recommend_present is False:
            for xml_reg in xml_file.findall('reg'):
                xml_regs.append({'bitfield': xml_reg.get('bitfield'), 'path': xml_reg.get('path')})
        elif bitfield_present is True and recommend_present is True:
            for xml_reg in xml_file.findall('reg'):
                # print(xml_reg.attrib.keys())
                if('desc' in xml_reg.attrib.keys()):
                    xml_regs.append({'bitfield':xml_reg.get('bitfield'),
                                     'recommend':hex(int(xml_reg.get('recommend'), 16)).rstrip('L'), # string to int, and to hex
                                     'path':xml_reg.get('path'),
                                     'desc':xml_reg.get('desc')})
                else:
                    xml_regs.append({'bitfield': xml_reg.get('bitfield'),
                                     'recommend': hex(int(xml_reg.get('recommend'), 16)).rstrip('L'),
                                     'path': xml_reg.get('path'),
                                     'desc': 'n/a'})
        else:
            raise TypeError('incorrect arguments; you need to have bitfields if you have recommends')

        xml_regs = [xml_reg for xml_reg in xml_regs if xml_reg['path'] is not None]
        xml_regs_df = pandas.DataFrame(xml_regs) # dict list to dataframe
        return xml_regs_df

    def xml_to_dictlist(self, xml_path):
        """
        read the xml file of registers and convert them to list of dicts

        :param xml_path:
        :return:
        """
        xml_file = etree.parse(xml_path)
        regs = []
        for reg in xml_file.findall('reg'):
            regs.append(reg.attrib)
        return regs

    def loadcsv_mm14(self, csv_path, num_true, num_false, step_size):
        """
        load mm14 raw data from mm14 v1.5.1.55
        :param csv_path:
        :param num_true: number to represent the duration of the workload
        :param num_false: number to represent both ends of the workload
        :param step_size: increment for the next workload
        :return: df
        """
        df_pwr_data = pandas.read_csv(csv_path, na_values=['.'], dtype=numpy.float)
        print(df_pwr_data)
        df_mm14_workloads = pandas.DataFrame(index=df_pwr_data.index,
                                             columns=['onenote', 'chrome', 'winzip', 'idle_0', 'word', 'powerpoint',
                                                      'acrobat', 'idle_1', 'outlook', 'excel', 'idle_2'],
                                             dtype=numpy.float)

        # set up df_mm14_workloads
        row_count = df_pwr_data.shape[0]
        # onenote
        df_mm14_workloads.iloc[:int(math.ceil(row_count * 0.05)), 0] = num_true
        df_mm14_workloads.iloc[0, 0] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.05)), 0] = num_false
        # chrome
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.05) + 2):int(math.ceil(row_count * 0.28)), 1] = num_true + step_size
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.05) + 1), 1] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.28)), 1] = num_false
        # winzip
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.28) + 2):int(math.ceil(row_count * 0.29)), 2] = num_true + step_size * 2
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.28) + 1), 2] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.29)), 2] = num_false
        # idle_0
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.29) + 2):int(math.ceil(row_count * 0.54)), 3] = num_true + step_size * 3
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.29) + 1), 3] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.54)), 3] = num_false
        # word
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.54) + 2):int(math.ceil(row_count * 0.6)), 4] = num_true + step_size * 4
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.54) + 1), 4] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.6)), 4] = num_false
        # powerpoint
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.6) + 2):int(math.ceil(row_count * 0.61)), 5] = num_true + step_size * 5
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.6) + 1), 5] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.61)), 5] = num_false
        # acrobat
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.61) + 2):int(math.ceil(row_count * 0.69)), 6] = num_true + step_size * 6
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.61) + 1), 6] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.69)), 6] = num_false
        # idle_1
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.69) + 2):int(math.ceil(row_count * 0.82)), 7] = num_true + step_size * 7
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.69) + 1), 7] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.82)), 7] = num_false
        # outlook
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.82) + 2):int(math.ceil(row_count * 0.84)), 8] = num_true + step_size * 8
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.82) + 1), 8] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.84)), 8] = num_false
        # excel
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.84) + 2):int(math.ceil(row_count * 0.92)), 9] = num_true + step_size * 9
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.84) + 1), 9] = num_false
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.92)), 9] = num_false
        # idle_2
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.92) + 2):, 10] = num_true + step_size * 10
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.92) + 1), 10] = num_false
        df_mm14_workloads.iloc[-1, 10] = num_false

        # combine the dataframes
        print(df_pwr_data.head(10))
        df = pandas.concat([df_pwr_data, df_mm14_workloads], axis=1)
        return df


    """ others """

    def subtract(self, a, b):
        """

        :param a:
        :param b:
        :return:
        """
        sub = a-b
        return sub