# Copyright 2012-2015 ADVANCED MICRO DEVICES, INC. All Rights Reserved.
#
# This software and any related documentation (the "Materials") are the
# confidential proprietary information of AMD. Unless otherwise provided
# in a software agreement specifically licensing the Materials, the Materials
# are provided in confidence and may not be distributed, modified, or
# reproduced in whole or in part by any means.
#
# LIMITATION OF LIABILITY: THE MATERIALS ARE PROVIDED "AS IS" WITHOUT ANY
# EXPRESS OR IMPLIED WARRANTY OF ANY KIND, INCLUDING BUT NOT LIMITED TO
# WARRANTIES OF MERCHANTABILITY, NONINFRINGEMENT, TITLE, FITNESS FOR ANY
# PARTICULAR PURPOSE, OR WARRANTIES ARISING FORM CONDUCT, COURSE OF DEALING,
# OR USAGE OF TRADE.  IN NO EVENT SHALL AMD OR ITS LICENSORS BE LIABLE FOR
# ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF
# PROFITS, BUSINESS INTERRUPTION, OR LOSS OF INFORMATION) ARISING OUT OF THE
# USE OF OR INABILITY TO USE THE MATERIALS, EVEN IF AMD HAS BEEN ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGES.  BECAUSE SOME JURISDICTIONS PROHIBIT THE
# EXCLUSION OR LIMITATION OF LIABILITY FOR CONSEQUENTIAL OR INCIDENTAL DAMAGES,
# THE ABOVE LIMITATION MAY NOT APPLY TO YOU.
#
# AMD does not assume any responsibility for any errors which may appear in the
# Materials nor any responsibility to support or update the Materials.  AMD
# retains the right to modify the Materials at any time, without notice,
# and is not obligated to provide such modified Materials to you.
#
# NO SUPPORT OBLIGATION: AMD is not obligated to furnish, support, or make any
# further information, software, technical information, know-how, or show-how
# available to you.
#
# U.S. GOVERNMENT RESTRICTED RIGHTS: The Materials are provided with
# "RESTRICTED RIGHTS." Use, duplication, or disclosure by the Government
# is subject to the restrictions as set forth in FAR 52.227-14 and DFAR
# 252.227-7013, et seq., or its successor.  Use of the Materials by the
# Government constitutes acknowledgement of AMD's proprietary rights in them.

import Kysy

import PythonTest

platform = PythonTest.platform
core_topo = platform.coreTopology()

print "\nPRINTING BASIC NODE ATTRIBUTES"
#! [register_access]
node0 = platform.regSetByPath( "LegacyDB.0::UNB.0::" )
print "Num dcts = {0}".format( len( node0.instancesOf("MCT", Kysy.RECURSIVE) ) )
print "Num functions = {0}".format( len( node0.regSets() ) )

print "\nREADING A SPECIFIC REGISTER"
device_vendor_id = platform.regByPath( "LegacyDB.0::UNB.0::F0.0::Device/Vendor ID" )
device_vendor_id.read()

print "\nPRINTING REGISTER RESULTS FOR DEVICE/VENDOR ID"
print "Device/Vendor ID = {0:#x}".format(device_vendor_id.value())

print "\nREADING A BATCH OF REGISTERS"
all_fn1 = platform.createRegisterBatch()
fn1 = platform.regSetByPath( "LegacyDB.0::UNB.0::F1.0::" )
all_fn1.addRead( fn1 )
all_fn1.execute()

print "\nPRINTING ALL PCI FUNCTION 1 REGISTERS FROM NODE 0"
for reg in fn1.regs():
  print "{0} ({1}) = {2:#x}".format(reg.definition().name(), reg.address(), reg.value())
#! [register_access]

#! [io_register_access]
port = Kysy.IORegister.create( 0x80, Kysy.IO_DWORD, platform.platformAccess() )
port.read()
print "IO port 0x80 current value = {0:#x}".format(port.value())
port.value( 0x42 )
port.write()
port.read()
print "IO port 0x80 new value = {0:#x}".format(port.value())
#! [io_register_access]

#! [pci_register_access]
print "\nCREATING PCI REGISTER AND READING IN A BATCH"
pci_reg= Kysy.PCIRegister.create(platform.platformAccess(), 0x0, 0x18, 0x0, 0x0)
batch_pci_reg = platform.createRegisterBatch()
batch_pci_reg.addRead(pci_reg)
batch_pci_reg.execute()
print "D18F0x00 read in a batch = {0:#x}".format(pci_reg.value())
#! [pci_register_access]


# Testing MSR write
print "\nWRITING TO MSR\n";
cores =  core_topo.cores()
PUBLIC_MSR_NAMESTR       = 0xC0010030
MSR_WRITE_DATA           = 0x0DEADBEEFC001C0DE
for core in cores:
    msr_reg = core.msr().reg( PUBLIC_MSR_NAMESTR )
    msr_reg.read();
    restore_val = msr_reg.value()
    msr_reg.value(MSR_WRITE_DATA);

    if MSR_WRITE_DATA != msr_reg.value():
        raise Exception("Register value should match.")

    msr_reg.write();
    msr_reg.read();
    print "Value after MSR write -  {0:#x}".format(msr_reg.value())
    msr_reg.value(restore_val);
    msr_reg.write();
    msr_reg.read();
    print "value after restore MSR -  {0:#x}".format(msr_reg.value())


# Language-specific toString
b = Kysy.BitVector(0xc001c0de)
if "{0}".format(b) != "< BitVector: numBits=32, value=0xC001C0DE >":
  raise Exception("Language-specific toString failed")

if (PythonTest.hdt != None):
  PythonTest.hdt.cpuDebug().exitDebug()

# vim:ts=2:sw=2:et
