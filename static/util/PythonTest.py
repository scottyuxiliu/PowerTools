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

#! [include]
import sys, os, platform
load_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Python"))
sys.path.append(load_dir)
import KysyEnvironment, Kysy
#! [include]

#! [init]
import argparse

#! [exceptions]
try:
  Kysy.StubPlatform.create "does", "not", "exist"
except RuntimeError as e:
  print("Exception: %s\n" % str(e))
#! [exceptions]

parser = argparse.ArgumentParser(description='Sample parser of args to support different target access methods')
parser.add_argument('--yaap', action="store", dest="yaap", help='Wombat IP address')
parser.add_argument('--hdt', action="store", dest="hdt", help='Wombat IP address (deprecated)')
parser.add_argument('--sim', nargs='?', const='sim', default='default')

args = parser.parse_args()

platform = None
wombat = None
hdt = None
sim = None

# Parse out the args and construct a platform instance
if (args.yaap != None):
  wombat = Kysy.Wombat.create(args.yaap)
  platform = wombat.platform()
  # Enter debug mode before the sample test
  wombat.cpuDebug().requestDebug()
elif (args.hdt != None):
  hdt = Kysy.HDTYaapDevice.create(args.hdt)
  platform = hdt.platform()
  # Enter debug mode before the sample test
  hdt.cpuDebug().requestDebug()
elif (args.sim != None and args.sim == 'sim'):
  # We connect to an existing SimNow session. Hence passing in an empty string.
  sim = Kysy.SimNowDevice.create('')
  platform = sim.platform()
  sim.cpuDebug().requestDebug()
else:
  # Construct a native platform
  platform = Kysy.Platform.create()
#! [init]

def to_mb(value):
  return value / 1024 / 1024

# vim:ts=2:sw=2:et
