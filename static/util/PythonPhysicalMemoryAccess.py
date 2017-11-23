# Copyright 2012-2016 ADVANCED MICRO DEVICES, INC. All Rights Reserved.
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

mem_topo = PythonTest.platform.memoryTopology()

print "\nMAP PHYSICAL MEMORY and READ"
if PythonTest.platform.platformAccess().hierarchyInfos()[0].chipInfo().cpuid().family() < 0x17:
  print "\n\tSkipping because test requires a SOC15 target\n"
else:
  #! [map_memory]
  baseaddress = 0x20
  size = Kysy.Bytes(10)
  mem_mapped = Kysy.PhysicalMemorySpace.mapMemory(PythonTest.platform.platformAccess(), Kysy.PPRCoreTopologyPhysicalIDs(0, 0, 0, 0, 0), baseaddress, size, Kysy.MEMORY_DESTINATION_AUTO, Kysy.MEMORY_TYPE_AUTO)
  mem_mapped.read
  #! [map_memory]

  mem_range = mem_topo.nodes()[0].range()

  if PythonTest.hdt == None and PythonTest.sim == None:
    print "\nALLOCATE PHYSICAL MEMORY and WRITE"
    #! [allocate_memory]
    mem_allocated = Kysy.PhysicalMemorySpace.allocateMemory(PythonTest.platform.platformAccess(), Kysy.PPRCoreTopologyPhysicalIDs(0, 0, 0, 0, 0), mem_range, size, Kysy.MEMORY_DESTINATION_AUTO, Kysy.MEMORY_TYPE_AUTO)
    mem_allocated.fill( 0x0 )
    for i in range(size.value()):
      mem_allocated.byte(i,i)

    mem_allocated.write
    #! [allocate_memory]

if (PythonTest.hdt != None):
  PythonTest.hdt.cpuDebug().exitDebug()

# vim:ts=2:sw=2:et
