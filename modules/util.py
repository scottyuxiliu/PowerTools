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

        self.socket_id = 0
        self.die_id = 0
        self.ccx_id = 0
        self.core_id = 0
        self.thread_id = 0
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

    def read_physical_memory(self):
        pprCoreTopoIDs = Kysy.PPRCoreTopologyPhysicalIDs(0, 0, 0, 0, 0)
        bytes = Kysy.Bytes(0x4)
        mem = Kysy.PhysicalMemorySpace.mapMemory(self.platform.platformAccess(),
                                                 pprCoreTopoIDs,
                                                 0xFED80E78,
                                                 bytes,
                                                 Kysy.MEMORY_DESTINATION_MMIO,
                                                 Kysy.MEMORY_TYPE_UNCACHEABLE,
                                                 Kysy.MEMORY_ACCESS_SIZE_64BIT)
        mem.fill(0)
        mem.read()
        return 0

    def read_smn_buffer(self,
                        smn_address,
                        return_type='hex',
                        verbose=False,
                        number_of_bytes_to_read=4,
                        number_of_read_attempts=4):
        """

        :param smn_address: SMN address doesn't need to be in 0x format. It should be an integer.
        :param return_type:
        :param verbose:
        :param number_of_bytes_to_read:
        :param number_of_read_attempts:
        :return:
        """
        smn_axi_buffer_access_object = Kysy.SMNAxiBufferAccess.create(self.platform,
                                                                      self.socket_id,
                                                                      self.die_id,
                                                                      smn_address,
                                                                      number_of_bytes_to_read,
                                                                      number_of_read_attempts)
        smn_axi_buffer_access_object.read()

        if return_type == 'hex':
            if verbose is True:
                print ("reading SMN buffer address {0}...".format(hex(smn_address).rstrip('L')))
            value = hex(smn_axi_buffer_access_object.dword(0)).rstrip('L')
            if verbose is True:
                print("    value at address {0} is {1}".format(hex(smn_address).rstrip('L'), value))
        elif return_type == 'int':
            if verbose is True:
                print ("reading SMN buffer address {0}...".format(hex(smn_address).rstrip('L')))
            value = smn_axi_buffer_access_object.dword(0)
            if verbose is True:
                print("    value at address {0} is {1}".format(hex(smn_address).rstrip('L'), value))
        else:
            raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

        return value

    def write_smn_buffer(self,
                         smn_address,
                         smn_data,
                         verbose=False,
                         number_of_bytes_to_read=4,
                         number_of_read_attempts=4):
        """

        :param smn_address: SMN address doesn't need to be in 0x format. It should be an integer.
        :param smn_data: SMN data should be an integer.
        :param verbose:
        :param number_of_bytes_to_read:
        :param number_of_read_attempts:
        :return:
        """
        smn_axi_buffer_access_object = Kysy.SMNAxiBufferAccess.create(self.platform,
                                                                      self.socket_id,
                                                                      self.die_id,
                                                                      smn_address,
                                                                      number_of_bytes_to_read,
                                                                      number_of_read_attempts)
        smn_axi_buffer_access_object.read()
        if verbose is True:
            print ("writing {0} to SMN buffer address {1}...".format(hex(smn_data).rstrip('L'), hex(smn_address).rstrip('L'))),
        smn_axi_buffer_access_object.dword(0, smn_data)
        smn_axi_buffer_access_object.write()
        if verbose is True:  # read back when verbose is true
            print ("done")
            time.sleep(2)
            smn_axi_buffer_access_object.read()
            print("    value at address {0} is {1}".format(hex(smn_address).rstrip('L'),
                                                           hex(smn_data).rstrip('L')))

    def read_mp1_buffer(self,
                        mp1_address,
                        return_type='hex',
                        verbose=False,
                        number_of_bytes_to_read=4,
                        number_of_read_attempts=4):
        """

        :param mp1_address: MP1 address doesn't need to be in 0x format. It can be an integer.
        :param return_type:
        :param verbose:
        :param number_of_bytes_to_read:
        :param number_of_read_attempts:
        :return:
        """
        mp1_buffer_access_object = Kysy.MPBuffer.create(self.platform,
                                                        mp1_address,
                                                        number_of_bytes_to_read,
                                                        number_of_read_attempts,
                                                        self.die_id,
                                                        self.socket_id)
        mp1_buffer_access_object.read()

        if return_type == 'hex':
            if verbose is True:
                print ("reading MP1 buffer address {0}...".format(hex(mp1_address).rstrip('L')))
            value = hex(mp1_buffer_access_object.dword(0)).rstrip('L')
            if verbose is True:
                print("    value at address {0} is {1}".format(hex(mp1_address).rstrip('L'), value))
        elif return_type == 'int':
            if verbose is True:
                print ("reading MP1 buffer address {0}...".format(hex(mp1_address).rstrip('L')))
            value = mp1_buffer_access_object.dword(0)
            if verbose is True:
                print("    value at address {0} is {1}".format(hex(mp1_address).rstrip('L'), value))
        else:
            raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

        return value

    def write_mp1_buffer(self,
                         mp1_address,
                         mp1_data,
                         verbose=False,
                         number_of_bytes_to_read=4,
                         number_of_read_attempts=4):
        """

        :param mp1_address: SMN address doesn't need to be in 0x format. It should be an integer.
        :param mp1_data:
        :param verbose:
        :param number_of_bytes_to_read:
        :param number_of_read_attempts:
        :return:
        """
        mp1_buffer_access_object = Kysy.MPBuffer.create(self.platform,
                                                        mp1_address,
                                                        number_of_bytes_to_read,
                                                        number_of_read_attempts,
                                                        self.die_id,
                                                        self.socket_id)
        mp1_buffer_access_object.read()

        if verbose is True:
            print ("writing {0} to MP1 buffer address {1}...".format(hex(mp1_data).rstrip('L'), hex(mp1_address).rstrip('L'))),
        mp1_buffer_access_object.dword(0, mp1_data)
        mp1_buffer_access_object.write()
        if verbose is True:  # read back when verbose is true
            print ("done")
            time.sleep(2)
            mp1_buffer_access_object.read()
            print("    value at address {0} is {1}".format(hex(mp1_address).rstrip('L'),
                                                           hex(mp1_data).rstrip('L')))

    def read_register(self, register_path, return_type='hex', verbose=False, log_duration=1, log_period=1):
        """
        read register several times, returns a dataframe with the access_address and value[0...n]
        :param register_path:
        :param return_type: return hex or int
        :param verbose: output all the messages
        :param log_duration: number of seconds to log
        :param log_period: number of seconds to wait between two reads
        :return: value if reading once, dictionary if reading several times
        """

        repeat = log_duration / log_period

        # if reading only once, return the value
        if repeat == 1:
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
        else:
            dict_list = {"access_address": register_path}
            for i in range(repeat):
                register = self.platform.regByPath(register_path)
                register.read()
                if return_type == 'hex':
                    if verbose is True:
                        print ("reading {0}...".format(register_path))
                        value = hex(register.value()).rstrip('L')
                    if verbose is True:
                        print("    {0} = {1}".format(register_path, value))
                    dict_list["value"+str(i)] = value
                elif return_type == 'int':
                    if verbose is True:
                        print ("reading {0}...".format(register_path))
                    value = register.value()
                    if verbose is True:
                        print("    {0} = {1}".format(register_path, value))
                        dict_list["value" + str(i)] = value
                else:
                    raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))
                time.sleep(log_period)
            return pandas.DataFrame(dict_list)

    def write_register(self, register_path, register_value, verbose=False):
        """
        write a value to a single register
        :param register_path:
        :param register_value:
        :param verbose:
        :return:
        """
        register = self.platform.regByPath(register_path)
        register.read()
        if verbose is True:
            print ("writing {0} to {1}...".format(hex(register_value).rstrip('L'), register_path)),
        register.value(register_value)
        register.write()
        if verbose is True:  # read back when verbose is true
            print ("done")
            time.sleep(2)
            register.read()
            print("    {0} = {1}".format(register_path, hex(register.value()).rstrip('L')))

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

        repeat = log_duration / log_period

        # if reading only once, return the value
        if repeat == 1:
            register = self.platform.regByPath(register_path)
            register.read()
            if return_type == 'hex':
                if verbose is True:
                    print ("reading {0}[{1}]...".format(register_path, register_field_name))
                value = hex(register.field(register_field_name).value()).rstrip('L')
                if verbose is True:
                    print("    {0}[{1}] = {2}".format(register_path, register_field_name, value))
            elif return_type == 'int':
                if verbose is True:
                    print ("reading {0}[{1}]...".format(register_path, register_field_name))
                value = register.field(register_field_name).value()
                if verbose is True:
                    print("    {0}[{1}] = {2}".format(register_path, register_field_name, value))
            else:
                raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))
            return value

        # if reading more than once, return the dataframe
        else:
            dictlist = []
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

    def write_register_field(self, register_path, register_field_name, register_field_value, verbose=False):

        """
        write a single register field
        :param register_path:
        :param register_field_name:
        :param register_field_value: needs to be a decimal integer
        :param verbose:
        :return:
        """
        register = self.platform.regByPath(register_path)
        register.read()
        if verbose is True:
            print ("writing {0} to {1}[{2}]...".format(hex(register_field_value).rstrip('L'),
                                                       register_path,
                                                       register_field_name)),
        register.field(register_field_name).value(register_field_value)
        register.write()
        if verbose is True:  # read back when verbose is true
            print ("done")
            time.sleep(2)
            register.read()
            print("    {0}[{1}] = {2}".format(register_path,
                                              register_field_name,
                                              hex(register.field(register_field_name).value()).rstrip('L')))

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
                        print ("reading {0}[{1}]...".format(reg_dict['access_address'], reg_dict['bitfield'])),
                    register = self.platform.regByPath(reg_dict['access_address'])
                    register.read()
                    if verbose is True:
                        print ("done")
                    reg_dict['value'+str(i)] = hex(register.field(reg_dict['bitfield']).value()).rstrip('L')
                    if verbose is True:
                        print ("    {0}[{1}] = {2}".format(reg_dict['access_address'],
                                                           reg_dict['bitfield'],
                                                           reg_dict['value'+str(i)]))
                    # check if recommend == value
                    if status_check is True:
                        if reg_dict['recommend'] == reg_dict['value'+str(i)]:
                            reg_dict.update({'status'+str(i): ''})
                        else:
                            reg_dict.update({'status'+str(i): 'BAD'})

            elif return_type == 'int':
                for reg_dict in regs_dictlist:
                    if verbose is True:
                        print ("reading {0}[{1}]...".format(reg_dict['access_address'], reg_dict['bitfield'])),
                    register = self.platform.regByPath(reg_dict['access_address'])
                    register.read()
                    if verbose is True:
                        print ("done")
                    reg_dict['value'+str(i)] = register.field(reg_dict['bitfield']).value()
                    if verbose is True:
                        print ("    {0}[{1}] = {2}".format(reg_dict['access_address'],
                                                           reg_dict['bitfield'],
                                                           reg_dict['value'+str(i)]))

                    if status_check is True:
                        if reg_dict['recommend'] == hex(reg_dict['value'+str(i)]).rstrip('L'):  # convert hex to int
                            reg_dict.update({'status'+str(i): ''})
                        else:
                            reg_dict.update({'status'+str(i): 'BAD'})
            else:
                raise TypeError('user passed in {0}, but return type can only be hex or int'.format(return_type))

            time.sleep(log_period)

        return pandas.DataFrame(regs_dictlist)

    def write_registers_in_dataframe(self, registers_dataframe, verbose=False):
        """
        the registers_dataframe must contain path and recommend fields
        :param registers_dataframe: recommend field must be number format
        :param verbose:
        :return:
        """
        regs_dictlist = registers_dataframe.to_dict('records')
        for reg_dict in regs_dictlist:
            self.write_register(reg_dict['access_address'], reg_dict['recommend'], verbose)

    def write_register_fields_in_dataframe(self, registers_dataframe, verbose=False):
        """
        the registers_dataframe must contain path, bitfield and recommend fields
        :param registers_dataframe:
        :param verbose: print out each register read
        :return:
        """
        regs_dictlist = registers_dataframe.to_dict('records')
        for reg_dict in regs_dictlist:
            self.write_register_field(reg_dict['access_address'], reg_dict['bitfield'], int(reg_dict['recommend'], 16), verbose)

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

        df = self.xml_to_dataframe(xml_file_path)
        df = self.read_registers_in_dataframe(df, return_type, verbose, log_duration, log_period)
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
        :return: self.read_register_fields_in_dataframe(df, return_type, verbose, log_duration, log_period, status_check)
        """

        df = self.xml_to_dataframe(xml_file_path)
        df = self.read_register_fields_in_dataframe(df, return_type, verbose, log_duration, log_period, status_check)
        if results_csv_path is None:
            return df
        else:
            df.to_csv(results_csv_path)
            return df

    def write_register_fields_in_xml_file(self, xml_path, verbose=False):
        """

        :param xml_path:
        :param verbose:
        :return:
        """

        df = self.xml_to_dataframe(xml_path)
        self.write_register_fields_in_dataframe(df, verbose)

    def read_all_in_xml_file(self,
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
        :return: self.read_register_fields_in_dataframe(df, return_type, verbose, log_duration, log_period, status_check)
        """

        dict_list = self.xml_to_dictlist(xml_file_path)
        df = self.read_all_in_dictlist(dict_list, return_type, verbose, log_duration, log_period, status_check)
        if results_csv_path is None:
            return df
        else:
            df.to_csv(results_csv_path)
            return df

    def write_all_in_xml_file(self, xml_path, verbose=False):
        """

        :param xml_path:
        :param verbose:
        :return:
        """

        dict_list = self.xml_to_dictlist(xml_path)
        self.write_all_in_dictlist(dict_list, verbose)

    def read_all_in_dictlist(self,
                             dictlist,
                             return_type='hex',
                             verbose=False,
                             log_duration=1,
                             log_period=1,
                             status_check=False):
        """

        :param dictlist:
        :param return_type:
        :param verbose:
        :param log_duration:
        :param log_period:
        :param status_check:
        :return:
        """
        repeat = log_duration / log_period

        if repeat == 1:
            for dict_item in dictlist:
                if dict_item['access_method'] == 'reg_by_path':
                    dict_item['value'] = self.read_register_field(dict_item['access_address'],
                                                                  dict_item['bitfield'],
                                                                  return_type,
                                                                  verbose,
                                                                  log_duration,
                                                                  log_period)
                elif dict_item['access_method'] == 'smn_buffer':
                    dict_item['value'] = self.read_smn_buffer(int(dict_item['access_address'], 16), 'hex', True)
                elif dict_item['access_method'] == 'mp1_buffer':
                    dict_item['value'] = self.read_mp1_buffer(int(dict_item['access_address'], 16), 'hex', True)
                else:
                    raise TypeError('unrecognized access_method {0}. access_method can only be reg_by_path, smn_buffer or mp1_buffer'.format(dict_item['access_method']))
            return pandas.DataFrame(dictlist)
        else:
            for i in range(repeat):
                for dict_item in dictlist:
                    if dict_item['access_method'] == 'reg_by_path':
                        dict_item['value'+str(i)] = self.read_register_field(dict_item['access_address'],
                                                                             dict_item['bitfield'],
                                                                             return_type,
                                                                             verbose,
                                                                             1,
                                                                             1)
                    elif dict_item['access_method'] == 'smn_buffer':
                        dict_item['value'+str(i)] = self.read_smn_buffer(int(dict_item['access_address'], 16), 'hex', True)
                    elif dict_item['access_method'] == 'mp1_buffer':
                        dict_item['value'+str(i)] = self.read_mp1_buffer(int(dict_item['access_address'], 16), 'hex', True)
                    else:
                        raise TypeError('unrecognized access_method {0}. access_method can only be reg_by_path, smn_buffer or mp1_buffer'.format(dict_item['access_method']))

                time.sleep(log_period)

            return pandas.DataFrame(dictlist)

    def write_all_in_dictlist(self, dictlist, verbose=False):
        """

        :param dictlist:
        :param verbose:
        :return:
        """

        for dict_item in dictlist:
            if dict_item['access_method'] == 'reg_by_path':
                self.write_register_field(dict_item['access_address'], dict_item['bitfield'], int(dict_item['recommend'], 16), verbose)
            elif dict_item['access_method'] == 'smn_buffer':
                self.write_smn_buffer(int(dict_item['access_address'], 16), int(dict_item['recommend'], 16), verbose)
            elif dict_item['access_method'] == 'mp1_buffer':
                self.write_mp1_buffer(int(dict_item['access_address'], 16), int(dict_item['recommend'], 16), verbose)
            else:
                raise TypeError('unrecognized access_method {0}. access_method can only be reg_by_path, smn_buffer or mp1_buffer'.format(dict_item['access_method']))

    """ data loading section """

    @staticmethod
    def xml_to_dictlist(xml_path):
        """
        read the xml file of registers and convert them to list of dicts

        :param xml_path:
        :return:
        """
        xml_file = etree.parse(xml_path)
        xml_items = []
        for xml_item in xml_file.findall('reg'):
            if xml_item.attrib['recommend'] is not None and xml_item.attrib['access_method'] is not None and xml_item.attrib['address'] is not None:
                xml_items.append({'bitfield': xml_item.get('bitfield'),
                                  'recommend': hex(int(xml_item.get('recommend'), 16)).rstrip('L'),  # string to int, and to hex
                                  'access_method': xml_item.get('access_method'),
                                  'access_address': xml_item.get('access_address'),
                                  'desc': xml_item.get('desc')})
        return xml_items

    @staticmethod
    def xml_to_dataframe(xml_path):
        """
        read the xml file of registers and convert them to a dataframe
        xml_item.attrib returns a dictionary of attributes and their values
        :param xml_path:
        :return: df
        """
        xml_file = etree.parse(xml_path)
        xml_items = []
        for xml_item in xml_file.findall('reg'):
            if xml_item.attrib['recommend'] is not None and xml_item.attrib['access_method'] is not None and xml_item.attrib['address'] is not None:
                xml_items.append({'bitfield': xml_item.get('bitfield'),
                                  'recommend': hex(int(xml_item.get('recommend'), 16)).rstrip('L'),
                                  # string to int, and to hex
                                  'access_method': xml_item.get('access_method'),
                                  'access_address': xml_item.get('access_address'),
                                  'desc': xml_item.get('desc')})

        xml_regs_df = pandas.DataFrame(xml_items)  # dict list to dataframe
        return xml_regs_df

    @staticmethod
    def loadcsv_mm14(csv_path, columns_to_plot, workload_lower_bound_value, workload_upper_bound_value, output_csv_path=None):
        """
        load mm14 raw data from mm14 v1.5.1.55
        :param csv_path:
        :param columns_to_plot: list of columns to plot
        :param workload_upper_bound_value: number to represent the duration of the workload
        :param workload_lower_bound_value: number to represent both ends of the workload
        :return: df
        """
        step_size = (workload_upper_bound_value - workload_lower_bound_value) / 10
        df_pwr_data = pandas.read_csv(csv_path, na_values=['.'], dtype=numpy.float)


        df_mm14_workloads = pandas.DataFrame(index=df_pwr_data.index,
                                             columns=['onenote', 'chrome', 'winzip', 'idle_0', 'word', 'powerpoint',
                                                      'acrobat', 'idle_1', 'outlook', 'excel', 'idle_2'],
                                             dtype=numpy.float)

        # set up df_mm14_workloads
        row_count = df_pwr_data.shape[0]
        # onenote
        df_mm14_workloads.iloc[:int(math.ceil(row_count * 0.05)), 0] = workload_lower_bound_value
        df_mm14_workloads.iloc[0, 0] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.05)), 0] = workload_lower_bound_value
        # chrome
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.05) + 2):int(math.ceil(row_count * 0.28)), 1] = workload_lower_bound_value + step_size
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.05) + 1), 1] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.28)), 1] = workload_lower_bound_value
        # winzip
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.28) + 2):int(math.ceil(row_count * 0.29)), 2] = workload_lower_bound_value + step_size * 2
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.28) + 1), 2] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.29)), 2] = workload_lower_bound_value
        # idle_0
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.29) + 2):int(math.ceil(row_count * 0.54)), 3] = workload_lower_bound_value + step_size * 3
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.29) + 1), 3] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.54)), 3] = workload_lower_bound_value
        # word
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.54) + 2):int(math.ceil(row_count * 0.6)), 4] = workload_lower_bound_value + step_size * 4
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.54) + 1), 4] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.6)), 4] = workload_lower_bound_value
        # powerpoint
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.6) + 2):int(math.ceil(row_count * 0.61)), 5] = workload_lower_bound_value + step_size * 5
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.6) + 1), 5] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.61)), 5] = workload_lower_bound_value
        # acrobat
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.61) + 2):int(math.ceil(row_count * 0.69)), 6] = workload_lower_bound_value + step_size * 6
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.61) + 1), 6] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.69)), 6] = workload_lower_bound_value
        # idle_1
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.69) + 2):int(math.ceil(row_count * 0.82)), 7] = workload_lower_bound_value + step_size * 7
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.69) + 1), 7] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.82)), 7] = workload_lower_bound_value
        # outlook
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.82) + 2):int(math.ceil(row_count * 0.84)), 8] = workload_lower_bound_value + step_size * 8
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.82) + 1), 8] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.84)), 8] = workload_lower_bound_value
        # excel
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.84) + 2):int(math.ceil(row_count * 0.92)), 9] = workload_lower_bound_value + step_size * 9
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.84) + 1), 9] = workload_lower_bound_value
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.92)), 9] = workload_lower_bound_value
        # idle_2
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.92) + 2):, 10] = workload_lower_bound_value + step_size * 10
        df_mm14_workloads.iloc[int(math.ceil(row_count * 0.92) + 1), 10] = workload_lower_bound_value
        df_mm14_workloads.iloc[-1, 10] = workload_lower_bound_value

        # combine the dataframes
        df = pandas.concat([df_pwr_data[columns_to_plot], df_mm14_workloads], axis=1)
        if output_csv_path is not None:
            df.to_csv(output_csv_path)
        return df


    """ others """

    @staticmethod
    def subtract(a, b):
        """

        :param a:
        :param b:
        :return:
        """
        sub = a-b
        return sub