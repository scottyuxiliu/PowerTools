$: << File.join( File.dirname(__FILE__) )
require 'Kysy'
require 'util'
#require 'debug_utils'
#require 'debug_utils'
require 'csv'

$SCRIPT_VERSION = 1

$STUB = 1 if ARGV[0].nil? 

if(!$STUB)
  printf("\n***********Using the Target Platform....***********")
  printf("\nEstablish Wombat connection...and establish objects for access handling")
  @wombat = Kysy::Wombat.create( ARGV[0], "SMU", "SMU" )  # Etc.getlogin
  @platform  = @wombat.platform
  platAccess = @platform.platformAccess()

  printf("\nPDM Entry is not required for this test")
  #@wombat.cpuDebug.requestDebug 

  printf("\nGather Wombat and SW Tool Info...")
  firmwares = @wombat.firmwares
  fw_FPGA = firmwares.find{ |x| x.type == "fpga" }
  fw_OS   = firmwares.find{ |x| x.type == "os" }
  printf("\n\n\
  Wombat info:\n\
    FPGA FW Version: %s\n\
    FPGA OS Version: %s\n\
    ",\
    fw_FPGA.version, fw_OS.version)

else
  # Create Stub Platform
  printf("\n ***********Using Stub Platform...***********\n\n")
  printf("\n Provide WombatIP addr as ARG in case if you want to run the test on Target Platform...\n\n")
  sleep(5)
  @platform = Kysy::StubPlatform.create(0x800F00)  # CZ = 0x660F00; ZP = 0x800F00 
  platAccess = @platform.platformAccess()
end

def stutter_efficiency(socket=0, die=0)
  #@wombat.cpuDebug.requestDebug
  @cstatecontrol = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::BCST::CstateControl")
  @cstatecontrol.read
  @cstatecontrol.field("DfCstateDisable").value(1)
  @cstatecontrol.write
  @perf_ctl_lo2 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlLo_PIE_n2")
  @perf_ctl_hi2 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlHi_PIE_n2")
  @perf_ctl_lo3 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlLo_PIE_n3")
  @perf_ctl_hi3 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlHi_PIE_n3")
  @perf_ctl_lo4 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlLo_PIE_n4")
  @perf_ctl_hi4 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlHi_PIE_n4")
  @perf_ctl_lo5 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlLo_PIE_n5")
  @perf_ctl_hi5 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlHi_PIE_n5")
  @perf_ctl_lo6 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlLo_PIE_n6")
  @perf_ctl_hi6 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlHi_PIE_n6")
  @perf_ctl_lo7 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlLo_PIE_n7")
  @perf_ctl_hi7 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtlHi_PIE_n7")
  
  @perf_ctl_lo2.value(0x0)
  @perf_ctl_lo2.write
  @perf_ctl_hi2.value(0x0)
  @perf_ctl_hi2.write
  @perf_ctl_lo3.value(0x0)
  @perf_ctl_lo3.write
  @perf_ctl_hi3.value(0x0)
  @perf_ctl_hi3.write
  @perf_ctl_lo4.value(0x0)
  @perf_ctl_lo4.write
  @perf_ctl_hi4.value(0x0)
  @perf_ctl_hi4.write
  @perf_ctl_lo5.value(0x0)
  @perf_ctl_lo5.write
  @perf_ctl_hi5.value(0x0)
  @perf_ctl_hi5.write
  @perf_ctl_lo6.value(0x0)
  @perf_ctl_lo6.write
  @perf_ctl_hi6.value(0x0)
  @perf_ctl_hi6.write
  @perf_ctl_lo7.value(0x0)
  @perf_ctl_lo7.write
  @perf_ctl_hi7.value(0x0)
  @perf_ctl_hi7.write
  
  @perf_count_Lo_n2 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrLo_n2")
  @perf_count_Hi_n2 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrHi_n2")
  @perf_count_Lo_n3 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrLo_n3")
  @perf_count_Hi_n3 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrHi_n3")
  @perf_count_Lo_n4 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrLo_n4")
  @perf_count_Hi_n4 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrHi_n4")
  @perf_count_Lo_n5 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrLo_n5")
  @perf_count_Hi_n5 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrHi_n5")
  @perf_count_Lo_n6 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrLo_n6")
  @perf_count_Hi_n6 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrHi_n6")
  @perf_count_Lo_n7 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrLo_n7")
  @perf_count_Hi_n7 = @platform.regByPath("PPR::DF::socket#{socket}::die#{die}::PIE0::PerfMonCtrHi_n7")
  
  
  @perf_count_Lo_n2.value(0x0)
  @perf_count_Lo_n2.write
  @perf_count_Hi_n2.value(0x0)
  @perf_count_Hi_n2.write
  @perf_count_Lo_n3.value(0x0)
  @perf_count_Lo_n3.write
  @perf_count_Hi_n3.value(0x0)
  @perf_count_Hi_n3.write
  @perf_count_Lo_n4.value(0x0)
  @perf_count_Lo_n4.write
  @perf_count_Hi_n4.value(0x0)
  @perf_count_Hi_n4.write
  @perf_count_Lo_n5.value(0x0)
  @perf_count_Lo_n5.write
  @perf_count_Hi_n5.value(0x0)
  @perf_count_Hi_n5.write
  @perf_count_Lo_n6.value(0x0)
  @perf_count_Lo_n6.write
  @perf_count_Hi_n6.value(0x0)
  @perf_count_Hi_n6.write
  @perf_count_Lo_n7.value(0x0)
  @perf_count_Lo_n7.write
  @perf_count_Hi_n7.value(0x0)
  @perf_count_Hi_n7.write

   #Count cycles in MM_ACTIVE
  @perf_ctl_lo2.value(0x00405284)
  @perf_ctl_lo2.write
  @perf_ctl_hi2.value(0x00000002)
  @perf_ctl_hi2.write
  #Count cycles in SAVE
  @perf_ctl_lo3.value(0x00404985)
  @perf_ctl_lo3.write
  @perf_ctl_hi3.value(0x00000002)
  @perf_ctl_hi3.write
  #Count cycles in RESTORE
  @perf_ctl_lo4.value(0x00405384)
  @perf_ctl_lo4.write
  @perf_ctl_hi4.value(0x00000002)
  @perf_ctl_hi4.write
  #Count cycles in RESTORE_DUP
  @perf_ctl_lo5.value(0x00401185)
  @perf_ctl_lo5.write
  @perf_ctl_hi5.value(0x00000002)
  @perf_ctl_hi5.write
  #Count cycles in FCSTATE = 2
  @perf_ctl_lo6.value(0x0040848B)
  @perf_ctl_lo6.write
  @perf_ctl_hi6.value(0x00000002)
  @perf_ctl_hi6.write
  # Total fclk Count cycles
  @perf_ctl_lo7.value(0x00400180)
  @perf_ctl_lo7.write
  @perf_ctl_hi7.value(0x00000002)
  @perf_ctl_hi7.write
  #@wombat.cpuDebug.exitDebug
  @cstatecontrol.read
  @cstatecontrol.field("DfCstateDisable").value(0)
  @cstatecontrol.write
  sleep(120)
  #@wombat.cpuDebug.requestDebug
  @cstatecontrol.read
  @cstatecontrol.field("DfCstateDisable").value(1)
  @cstatecontrol.write
  @perf_count_Lo_n2.read
  @perf_count_Hi_n2.read
  @perf_count_Lo_n3.read
  @perf_count_Hi_n3.read
  @perf_count_Lo_n4.read
  @perf_count_Hi_n4.read
  @perf_count_Lo_n5.read
  @perf_count_Hi_n5.read
  @perf_count_Lo_n6.read
  @perf_count_Hi_n6.read
  @perf_count_Lo_n7.read
  @perf_count_Hi_n7.read
  #@wombat.cpuDebug.exitDebug
  @cstatecontrol.read
  @cstatecontrol.field("DfCstateDisable").value(0)
  @cstatecontrol.write
  @perf_count_mm_active     = @perf_count_Hi_n2.value*(2**32) +  @perf_count_Lo_n2.value
  @perf_count_save          = @perf_count_Hi_n3.value*(2**32) +  @perf_count_Lo_n3.value
  @perf_count_restore       = @perf_count_Hi_n4.value*(2**32) +  @perf_count_Lo_n4.value
  @perf_count_restore_dup   = @perf_count_Hi_n5.value*(2**32) +  @perf_count_Lo_n5.value
  @perf_count_fcstate_2     = @perf_count_Hi_n6.value*(2**32) +  @perf_count_Lo_n6.value
  @perf_count_fclk          = @perf_count_Hi_n7.value*(2**32) +  @perf_count_Lo_n7.value
 
  puts "@perf_count_mm_active   #{@perf_count_mm_active}\n"
  puts "@perf_count_save        #{@perf_count_save}\n"
  puts "@perf_count_restore     #{@perf_count_restore}\n"
  puts "@perf_count_restore_dup #{@perf_count_restore_dup}\n"
  puts "@perf_count_fcstate_2   #{@perf_count_fcstate_2}\n"
  puts "@perf_count_fclk        #{@perf_count_fclk}\n"
  
  @effective_stutter_fclk_count = @perf_count_fclk - (@perf_count_mm_active + @perf_count_save + @perf_count_restore +@perf_count_restore_dup)
  
  @cstateresidency400          = (@perf_count_fcstate_2*3200).to_f/(@perf_count_fcstate_2*31+@perf_count_fclk).to_f
  puts "SR residency at DPM0 (400MHz) is   #{@cstateresidency400}\n"
  
  @cstateresidency933          = (@perf_count_fcstate_2*933).to_f/(@perf_count_fcstate_2*8.33+@perf_count_fclk).to_f
  puts "SR residency at DPM1 (933MHz) is   #{@cstateresidency933}\n"

  @cstateresidency1067          = (@perf_count_fcstate_2*1067).to_f/(@perf_count_fcstate_2*9.67+@perf_count_fclk).to_f
  puts "SR residency at DPM2 (1067MHz) is   #{@cstateresidency1067}\n"

  @cstateresidency1200          = (@perf_count_fcstate_2*1200).to_f/(@perf_count_fcstate_2*11+@perf_count_fclk).to_f
  puts "SR residency at DPM3 (1200MHz) is   #{@cstateresidency1200}\n"
  
  @stutterefficiency400          = (@perf_count_fcstate_2*3200).to_f/(@perf_count_fcstate_2*31+@effective_stutter_fclk_count).to_f
  puts "stutter efficiency at DPM0 (400MHz) is   #{@stutterefficiency400}\n"
  
  @stutterefficiency933          = (@perf_count_fcstate_2*933).to_f/(@perf_count_fcstate_2*8.33+@effective_stutter_fclk_count).to_f
  puts "stutter efficiency at DPM1 (933MHz) is   #{@stutterefficiency933}\n"

  @stutterefficiency1067          = (@perf_count_fcstate_2*1067).to_f/(@perf_count_fcstate_2*9.67+@effective_stutter_fclk_count).to_f
  puts "stutter efficiency at DPM2 (1067MHz) is   #{@stutterefficiency1067}\n"

  @stutterefficiency1200          = (@perf_count_fcstate_2*1200).to_f/(@perf_count_fcstate_2*11+@effective_stutter_fclk_count).to_f
  puts "stutter efficiency at DPM3 (1200MHz) is   #{@stutterefficiency1200}\n"
end

stutter_efficiency()