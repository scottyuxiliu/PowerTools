import numpy
import pandas

import sys
import time


class StutterEfficiency():
    """stutter efficiency class"""
    def __init__(self, util):
        self.util = util

    def read_stutter(self,
                     time_delay_in_sec=600,
                     number_of_runs=1,
                     require_pdm=False,
                     verbose=False,
                     result_csv_path=None):
        if require_pdm:
            stutter_efficiency_df = self.__log_with_pdm_mode(time_delay_in_sec, number_of_runs, verbose)
            if result_csv_path is not None:
                stutter_efficiency_df.to_csv(result_csv_path)
        else:
            stutter_efficiency_df = self.__log_without_pdm_mode(time_delay_in_sec,number_of_runs)
            if result_csv_path is not None:
                stutter_efficiency_df.to_csv(result_csv_path)
        return 0

    def __log_with_pdm_mode(self,time_delay_in_sec, number_of_runs, verbose):
        perf_ctl_lo1_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlLo_PIE_n1"
        perf_ctl_hi1_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlHi_PIE_n1"
        perf_ctl_lo2_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlLo_PIE_n2"
        perf_ctl_hi2_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlHi_PIE_n2"
        perf_ctl_lo3_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlLo_PIE_n3"
        perf_ctl_hi3_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlHi_PIE_n3"
        perf_ctl_lo4_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlLo_PIE_n4"
        perf_ctl_hi4_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlHi_PIE_n4"
        perf_ctl_lo5_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlLo_PIE_n5"
        perf_ctl_hi5_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlHi_PIE_n5"
        perf_ctl_lo6_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlLo_PIE_n6"
        perf_ctl_hi6_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlHi_PIE_n6"
        perf_ctl_lo7_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlLo_PIE_n7"
        perf_ctl_hi7_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtlHi_PIE_n7"
        perf_count_Lo_n1_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrLo_n1"
        perf_count_Hi_n1_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrHi_n1"
        perf_count_Lo_n2_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrLo_n2"
        perf_count_Hi_n2_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrHi_n2"
        perf_count_Lo_n3_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrLo_n3"
        perf_count_Hi_n3_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrHi_n3"
        perf_count_Lo_n4_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrLo_n4"
        perf_count_Hi_n4_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrHi_n4"
        perf_count_Lo_n5_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrLo_n5"
        perf_count_Hi_n5_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrHi_n5"
        perf_count_Lo_n6_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrLo_n6"
        perf_count_Hi_n6_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrHi_n6"
        perf_count_Lo_n7_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrLo_n7"
        perf_count_Hi_n7_path = "PPR::DF::socket0::die0::PIE0::PerfMonCtrHi_n7"

        data = []

        for i in range(number_of_runs):
            start_time = time.time()

            print("initializing counters...")
            self.util.enter_pdm_mode(verbose)
            self.util.write_register(perf_ctl_lo1_path, 0x0, verbose)
            self.util.write_register(perf_ctl_hi1_path, 0x0, verbose)
            self.util.write_register(perf_ctl_lo2_path, 0x0, verbose)
            self.util.write_register(perf_ctl_hi2_path, 0x0, verbose)
            self.util.write_register(perf_ctl_lo3_path, 0x0, verbose)
            self.util.write_register(perf_ctl_hi3_path, 0x0, verbose)
            self.util.write_register(perf_ctl_lo4_path, 0x0, verbose)
            self.util.write_register(perf_ctl_hi4_path, 0x0, verbose)
            self.util.write_register(perf_ctl_lo5_path, 0x0, verbose)
            self.util.write_register(perf_ctl_hi5_path, 0x0, verbose)
            self.util.write_register(perf_ctl_lo6_path, 0x0, verbose)
            self.util.write_register(perf_ctl_hi6_path, 0x0, verbose)
            self.util.write_register(perf_ctl_lo7_path, 0x0, verbose)
            self.util.write_register(perf_ctl_hi7_path, 0x0, verbose)
            self.util.write_register(perf_count_Lo_n1_path, 0x0, verbose)
            self.util.write_register(perf_count_Hi_n1_path, 0x0, verbose)
            self.util.write_register(perf_count_Lo_n2_path, 0x0, verbose)
            self.util.write_register(perf_count_Hi_n2_path, 0x0, verbose)
            self.util.write_register(perf_count_Lo_n3_path, 0x0, verbose)
            self.util.write_register(perf_count_Hi_n3_path, 0x0, verbose)
            self.util.write_register(perf_count_Lo_n4_path, 0x0, verbose)
            self.util.write_register(perf_count_Hi_n4_path, 0x0, verbose)
            self.util.write_register(perf_count_Lo_n5_path, 0x0, verbose)
            self.util.write_register(perf_count_Hi_n5_path, 0x0, verbose)
            self.util.write_register(perf_count_Lo_n6_path, 0x0, verbose)
            self.util.write_register(perf_count_Hi_n6_path, 0x0, verbose)
            self.util.write_register(perf_count_Lo_n7_path, 0x0, verbose)
            self.util.write_register(perf_count_Hi_n7_path, 0x0, verbose)

            #Count cycles in MM_ACTIVE
            self.util.write_register(perf_ctl_lo2_path, 0x00405284, verbose)
            self.util.write_register(perf_ctl_hi2_path, 0x00000002, verbose)
            #Count cycles in SAVE
            self.util.write_register(perf_ctl_lo3_path, 0x00404985, verbose)
            self.util.write_register(perf_ctl_hi3_path, 0x00000002, verbose)
            #Count cycles in RESTORE
            self.util.write_register(perf_ctl_lo4_path, 0x00405384, verbose)
            self.util.write_register(perf_ctl_hi4_path, 0x00000002, verbose)
            #Count cycles in RESTORE_DUP
            self.util.write_register(perf_ctl_lo5_path, 0x00401185, verbose)
            self.util.write_register(perf_ctl_hi5_path, 0x00000002, verbose)
            #Count cycles in FCSTATE = 2
            self.util.write_register(perf_ctl_lo6_path, 0x0040848B, verbose)
            self.util.write_register(perf_ctl_hi6_path, 0x00000002, verbose)
            #Count cycles in IDLE_ACTIVE
            self.util.write_register(perf_ctl_lo1_path, 0x00404084, verbose)
            self.util.write_register(perf_ctl_hi1_path, 0x00000002, verbose)
            #Total fclk Count cycles
            self.util.write_register(perf_ctl_lo7_path, 0x00400180, verbose)
            self.util.write_register(perf_ctl_hi7_path, 0x00000002, verbose)

            self.util.exit_pdm_mode()

            print("logging...")
            time.sleep(time_delay_in_sec)

            print("finished logging, combining high and low 32 bits...")
            self.util.enter_pdm_mode(verbose)
            idle_active = self.util.read_register(perf_count_Hi_n1_path, 'int', verbose)*(2**32) + self.util.read_register(perf_count_Lo_n1_path, 'int', verbose) #combine high 32 bits and low 32 bits
            mm_active = self.util.read_register(perf_count_Hi_n2_path, 'int', verbose)*(2**32) + self.util.read_register(perf_count_Lo_n2_path, 'int', verbose)
            save = self.util.read_register(perf_count_Hi_n3_path, 'int', verbose)*(2**32) + self.util.read_register(perf_count_Lo_n3_path, 'int', verbose)
            restore = self.util.read_register(perf_count_Hi_n4_path, 'int', verbose)*(2**32) + self.util.read_register(perf_count_Lo_n4_path, 'int', verbose)
            restore_dup = self.util.read_register(perf_count_Hi_n5_path, 'int', verbose)*(2**32) + self.util.read_register(perf_count_Lo_n5_path, 'int', verbose)
            fcstate_2 = self.util.read_register(perf_count_Hi_n6_path, 'int', verbose)*(2**32) + self.util.read_register(perf_count_Lo_n6_path, 'int', verbose)
            fclk = self.util.read_register(perf_count_Hi_n7_path, 'int', verbose)*(2**32) + self.util.read_register(perf_count_Lo_n7_path, 'int', verbose)
            self.util.exit_pdm_mode(verbose)

            print ("calculating residencies...")
            non_cstate_count = idle_active + mm_active + save + restore + restore_dup
            stutter_fclk_count = fclk - non_cstate_count

            stutter_fclk_norm_400 = fcstate_2*31 + stutter_fclk_count
            stutter_fclk_norm_933 = fcstate_2*8.33 + stutter_fclk_count
            stutter_fclk_norm_1067 = fcstate_2*9.67 + stutter_fclk_count
            stutter_fclk_norm_1200 = fcstate_2*11 + stutter_fclk_count

            fclk_norm_400 = fcstate_2*31 + fclk
            fclk_norm_933 = fcstate_2*8.33 + fclk
            fclk_norm_1067 = fcstate_2*9.67 + fclk
            fclk_norm_1200 = fcstate_2*11 + fclk

            cstate_count_400 = fclk_norm_400 - non_cstate_count
            cstate_count_933 = fclk_norm_933 - non_cstate_count
            cstate_count_1067 = fclk_norm_1067 - non_cstate_count
            cstate_count_1200 = fclk_norm_1200 - non_cstate_count

            print ("-------------------------------------------")
            print("idle_active = {0}".format(idle_active))
            print("mm_active = {0}".format(mm_active))
            print("save = {0}".format(save))
            print("restore = {0}".format(restore))
            print("restore_dup = {0}".format(restore_dup))
            print("fcstate_2 = {0}".format(fcstate_2))
            print("fclk = {0}".format(fclk))
            print("==================================")
            print("non_cstate_count = {0}".format(non_cstate_count))
            print("stutter_fclk_count = {0}".format(stutter_fclk_count))
            print("==================================")
            print("stutter_fclk_norm_400 = {0}".format(stutter_fclk_norm_400))
            print("stutter_fclk_norm_933 = {0}".format(stutter_fclk_norm_933))
            print("stutter_fclk_norm_1067 = {0}".format(stutter_fclk_norm_1067))
            print("stutter_fclk_norm_1200 = {0}".format(stutter_fclk_norm_1200))
            print("==================================")
            print("fclk_norm_400 = {0}".format(fclk_norm_400))
            print("fclk_norm_933 = {0}".format(fclk_norm_933))
            print("fclk_norm_1067 = {0}".format(fclk_norm_1067))
            print("fclk_norm_1200 = {0}".format(fclk_norm_1200))
            print("==================================")
            print("cstate_count_400 = {0}".format(cstate_count_400))
            print("cstate_count_933 = {0}".format(cstate_count_933))
            print("cstate_count_1067 = {0}".format(cstate_count_1067))
            print("cstate_count_1200 = {0}".format(cstate_count_1200))

            print("-----getting residency-----")
            cstate_residency_400 = (cstate_count_400*100)/(fclk_norm_400)
            cstate_residency_933 = (cstate_count_933*100)/(fclk_norm_933)
            cstate_residency_1067 = (cstate_count_1067*100)/(fclk_norm_1067)
            cstate_residency_1200 = (cstate_count_1200*100)/(fclk_norm_1200)

            low_power_residency_400 = (fcstate_2*3200)/(fclk_norm_400)
            low_power_residency_933 = (fcstate_2*933)/(fclk_norm_933)
            low_power_residency_1067 = (fcstate_2*1067)/(fclk_norm_1067)
            low_power_residency_1200 = (fcstate_2*1200)/(fclk_norm_1200)

            stutter_efficiency_400= (fcstate_2*3200)/(stutter_fclk_norm_400)
            stutter_efficiency_933= (fcstate_2*933)/(stutter_fclk_norm_933)
            stutter_efficiency_1067= (fcstate_2*1067)/(stutter_fclk_norm_1067)
            stutter_efficiency_1200= (fcstate_2*1200)/(stutter_fclk_norm_1200)

            # DF C-state residency - % of total time that we're not doing DMA or interrupt or saving/restoring state.  we could be servicing display stutter but that doesn't affect C-state %
            print("cstate_residency_400 = {0}".format(cstate_residency_400))
            print("cstate_residency_933 = {0}".format(cstate_residency_933))
            print("cstate_residency_1067 = {0}".format(cstate_residency_1067))
            print("cstate_residency_1200 = {0}".format(cstate_residency_1200))
            print("==================================")
            # low power residency - % of total time we are in low power state i.e fclk is at lower frequency.it gets deducted when we exit low power to service dma, interrupts, or do stutter
            # Low power residency = Cstate residency * stutter efficiency
            print("low_power_residency_400 = {0}".format(low_power_residency_400))
            print("low_power_residency_933 = {0}".format(low_power_residency_933))
            print("low_power_residency_1067 = {0}".format(low_power_residency_1067))
            print("low_power_residency_1200 = {0}".format(low_power_residency_1200))
            print("==================================")
            # stutter efficiency - % in low power after we've entered C-state, e.g. after all DMA and interrupt has stopped and we've saved state. Display SR traffic is responsible for this
            print("stutter_efficiency_400 = {0}".format(stutter_efficiency_400))
            print("stutter_efficiency_933 = {0}".format(stutter_efficiency_933))
            print("stutter_efficiency_1067 = {0}".format(stutter_efficiency_1067))
            print("stutter_efficiency_1200 = {0}".format(stutter_efficiency_1200))
            print("-----finished calculation-----")

            data.append({'read time (s)':time.time()-start_time,
                         'Cstate Residency 400MHz':cstate_residency_400,
                         'Cstate Residency 933MHz':cstate_residency_933,
                         'Cstate Residency 1067MHz':cstate_residency_1067,
                         'Cstate Residency 1200MHz':cstate_residency_1200,
                         'Low Power Residency 400MHz':low_power_residency_400,
                         'Low Power Residency 933MHz':low_power_residency_933,
                         'Low Power Residency 1067MHz':low_power_residency_1067,
                         'Low Power Residency 1200MHz':low_power_residency_1200,
                         'Stutter Efficiency 400MHz':stutter_efficiency_400,
                         'Stutter Efficiency 933MHz':stutter_efficiency_933,
                         'Stutter Efficiency 1067MHz':stutter_efficiency_1067,
                         'Stutter Efficiency 1200MHz':stutter_efficiency_1200})

        df = pandas.DataFrame(data)
        return df

    def __log_without_pdm_mode(self,time_delay_in_sec,number_of_runs):
        data = []

        for i in range(number_of_runs):
            start_time = time.time()

            cstatecontrol = self.platform.regByPath("PPR::DF::socket{0}::die{1}::BCST::CstateControl".format(self.socket,self.die))
            print("-----initialize perf counters-----")
            cstatecontrol.read()
            if cstatecontrol.field("DfCstateDisable").value() == 0:
                cstatecontrol.field("DfCstateDisable").value(1)
                cstatecontrol.write()
            perf_ctl_lo2 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlLo_PIE_n2".format(self.socket,self.die))
            perf_ctl_hi2 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlHi_PIE_n2".format(self.socket,self.die))
            perf_ctl_lo3 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlLo_PIE_n3".format(self.socket,self.die))
            perf_ctl_hi3 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlHi_PIE_n3".format(self.socket,self.die))
            perf_ctl_lo4 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlLo_PIE_n4".format(self.socket,self.die))
            perf_ctl_hi4 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlHi_PIE_n4".format(self.socket,self.die))
            perf_ctl_lo5 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlLo_PIE_n5".format(self.socket,self.die))
            perf_ctl_hi5 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlHi_PIE_n5".format(self.socket,self.die))
            perf_ctl_lo6 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlLo_PIE_n6".format(self.socket,self.die))
            perf_ctl_hi6 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlHi_PIE_n6".format(self.socket,self.die))
            perf_ctl_lo7 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlLo_PIE_n7".format(self.socket,self.die))
            perf_ctl_hi7 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtlHi_PIE_n7".format(self.socket,self.die))
            perf_ctl_lo2.value(0x0)
            perf_ctl_lo2.write()
            perf_ctl_hi2.value(0x0)
            perf_ctl_hi2.write()
            perf_ctl_lo3.value(0x0)
            perf_ctl_lo3.write()
            perf_ctl_hi3.value(0x0)
            perf_ctl_hi3.write()
            perf_ctl_lo4.value(0x0)
            perf_ctl_lo4.write()
            perf_ctl_hi4.value(0x0)
            perf_ctl_hi4.write()
            perf_ctl_lo5.value(0x0)
            perf_ctl_lo5.write()
            perf_ctl_hi5.value(0x0)
            perf_ctl_hi5.write()
            perf_ctl_lo6.value(0x0)
            perf_ctl_lo6.write()
            perf_ctl_hi6.value(0x0)
            perf_ctl_hi6.write()
            perf_ctl_lo7.value(0x0)
            perf_ctl_lo7.write()
            perf_ctl_hi7.value(0x0)
            perf_ctl_hi7.write()
            perf_count_Lo_n2 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrLo_n2".format(self.socket,self.die))
            perf_count_Hi_n2 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrHi_n2".format(self.socket,self.die))
            perf_count_Lo_n3 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrLo_n3".format(self.socket,self.die))
            perf_count_Hi_n3 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrHi_n3".format(self.socket,self.die))
            perf_count_Lo_n4 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrLo_n4".format(self.socket,self.die))
            perf_count_Hi_n4 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrHi_n4".format(self.socket,self.die))
            perf_count_Lo_n5 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrLo_n5".format(self.socket,self.die))
            perf_count_Hi_n5 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrHi_n5".format(self.socket,self.die))
            perf_count_Lo_n6 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrLo_n6".format(self.socket,self.die))
            perf_count_Hi_n6 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrHi_n6".format(self.socket,self.die))
            perf_count_Lo_n7 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrLo_n7".format(self.socket,self.die))
            perf_count_Hi_n7 = self.platform.regByPath("PPR::DF::socket{0}::die{1}::PIE0::PerfMonCtrHi_n7".format(self.socket,self.die))
            perf_count_Lo_n2.value(0x0)
            perf_count_Lo_n2.write()
            perf_count_Hi_n2.value(0x0)
            perf_count_Hi_n2.write()
            perf_count_Lo_n3.value(0x0)
            perf_count_Lo_n3.write()
            perf_count_Hi_n3.value(0x0)
            perf_count_Hi_n3.write()
            perf_count_Lo_n4.value(0x0)
            perf_count_Lo_n4.write()
            perf_count_Hi_n4.value(0x0)
            perf_count_Hi_n4.write()
            perf_count_Lo_n5.value(0x0)
            perf_count_Lo_n5.write()
            perf_count_Hi_n5.value(0x0)
            perf_count_Hi_n5.write()
            perf_count_Lo_n6.value(0x0)
            perf_count_Lo_n6.write()
            perf_count_Hi_n6.value(0x0)
            perf_count_Hi_n6.write()
            perf_count_Lo_n7.value(0x0)
            perf_count_Lo_n7.write()
            perf_count_Hi_n7.value(0x0)
            perf_count_Hi_n7.write()
            #Count cycles in MM_ACTIVE
            perf_ctl_lo2.value(0x00405284)
            perf_ctl_lo2.write()
            perf_ctl_hi2.value(0x00000002)
            perf_ctl_hi2.write()
            #Count cycles in SAVE
            perf_ctl_lo3.value(0x00404985)
            perf_ctl_lo3.write()
            perf_ctl_hi3.value(0x00000002)
            perf_ctl_hi3.write()
            #Count cycles in RESTORE
            perf_ctl_lo4.value(0x00405384)
            perf_ctl_lo4.write()
            perf_ctl_hi4.value(0x00000002)
            perf_ctl_hi4.write()
            #Count cycles in RESTORE_DUP
            perf_ctl_lo5.value(0x00401185)
            perf_ctl_lo5.write()
            perf_ctl_hi5.value(0x00000002)
            perf_ctl_hi5.write()
            #Count cycles in FCSTATE = 2
            perf_ctl_lo6.value(0x0040848B)
            perf_ctl_lo6.write()
            perf_ctl_hi6.value(0x00000002)
            perf_ctl_hi6.write()
            #Total fclk Count cycles
            perf_ctl_lo7.value(0x00400180)
            perf_ctl_lo7.write()
            perf_ctl_hi7.value(0x00000002)
            perf_ctl_hi7.write()
            cstatecontrol.field("DfCstateDisable").value(0)
            cstatecontrol.write()
            print("-----finished initializing perf counters-----")

            progress = time_delay_in_sec/100
            for i in range(0, time_delay_in_sec, progress):
                sys.stdout.write("\r{0}%".format((progress*i*100)/time_delay_in_sec))
                time.sleep(progress)
            sys.stdout.write("\r100%")
            print(" DONE!")

            print("-----start reading perf counters-----")
            cstatecontrol.read()
            if cstatecontrol.field("DfCstateDisable").value() == 0:
                cstatecontrol.field("DfCstateDisable").value(1)
                cstatecontrol.write()
            perf_count_Lo_n2.read()
            perf_count_Hi_n2.read()
            perf_count_Lo_n3.read()
            perf_count_Hi_n3.read()
            perf_count_Lo_n4.read()
            perf_count_Hi_n4.read()
            perf_count_Lo_n5.read()
            perf_count_Hi_n5.read()
            perf_count_Lo_n6.read()
            perf_count_Hi_n6.read()
            perf_count_Lo_n7.read()
            perf_count_Hi_n7.read()
            cstatecontrol.field("DfCstateDisable").value(0)
            cstatecontrol.write()
            print("-----finished reading perf counters-----")

            print("-----calculating-----")
            perf_count_mm_active=perf_count_Hi_n2.value()*(2**32) + perf_count_Lo_n2.value()
            perf_count_save=perf_count_Hi_n3.value()*(2**32) + perf_count_Lo_n3.value()
            perf_count_restore=perf_count_Hi_n4.value()*(2**32)+perf_count_Lo_n4.value()
            perf_count_restore_dup=perf_count_Hi_n5.value()*(2**32) + perf_count_Lo_n5.value()
            perf_count_fcstate_2=perf_count_Hi_n6.value()*(2**32) + perf_count_Lo_n6.value()
            perf_count_fclk=perf_count_Hi_n7.value()*(2**32) +perf_count_Lo_n7.value()

            effective_stutter_fclk_count = perf_count_fclk - (perf_count_mm_active + perf_count_save + perf_count_restore +perf_count_restore_dup)
            cstateresidency400= (perf_count_fcstate_2*3200)/(perf_count_fcstate_2*31+perf_count_fclk)
            cstateresidency933= (perf_count_fcstate_2*933)/(perf_count_fcstate_2*8.33+perf_count_fclk)
            cstateresidency1067= (perf_count_fcstate_2*1067)/(perf_count_fcstate_2*9.67+perf_count_fclk)
            cstateresidency1200= (perf_count_fcstate_2*1200)/(perf_count_fcstate_2*11+perf_count_fclk)
            stutterefficiency400= (perf_count_fcstate_2*3200)/(perf_count_fcstate_2*31+effective_stutter_fclk_count)
            stutterefficiency933= (perf_count_fcstate_2*933)/(perf_count_fcstate_2*8.33+effective_stutter_fclk_count)
            stutterefficiency1067= (perf_count_fcstate_2*1067)/(perf_count_fcstate_2*9.67+effective_stutter_fclk_count)
            stutterefficiency1200= (perf_count_fcstate_2*1200)/(perf_count_fcstate_2*11+effective_stutter_fclk_count)

            print("DF C-state residency at DPM0 (400MHz) is {0}".format(cstateresidency400))
            print("DF C-state residency at DPM1 (933MHz) is {0}".format(cstateresidency933))
            print("DF C-state residency at DPM2 (1067MHz) is {0}".format(cstateresidency1067))
            print("DF C-state residency at DPM3 (1200MHz) is {0}".format(cstateresidency1200))

            print("stutter efficiency at DPM0 (400MHz) is {0}".format(stutterefficiency400))
            print("stutter efficiency at DPM1 (933MHz) is {0}".format(stutterefficiency933))
            print("stutter efficiency at DPM2 (1067MHz) is {0}".format(stutterefficiency1067))
            print("stutter efficiency at DPM3 (1200MHz) is {0}".format(stutterefficiency1200))
            print("-----finished calculation-----")

            data.append({'read time (s)':time.time()-start_time,'stutter efficiency 400MHz':stutterefficiency400,'stutter efficiency 933MHz':stutterefficiency933,'stutter efficiency 1067MHz':stutterefficiency1067,'stutter efficiency 1200MHz':stutterefficiency1200})

        df = pandas.DataFrame(data)
        return df
