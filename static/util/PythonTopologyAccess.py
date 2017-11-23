import PythonTest

#! [core_topology]
platform = PythonTest.platform
core_topo = platform.coreTopology()
print "CORE TOPOLOGY"
for package in core_topo.packages():
  print "Package {0}".format(package.physicalID())
  for node in package.nodes():
    print "\tNode {0}".format(node.physicalID())
    for cu in node.computeUnits():
      print "\t\tCompute Unit {0}".format(cu.physicalID())
    for core in node.cores():
      print "\t\tCore {0} with APIC ID = {1}".format(core.physicalID(), core.apicID())
#! [core_topology]

print "\n\nMEMORY TOPOLOGY"
mem_topo = platform.memoryTopology()
print "TOM = {0} MB and TOM2 = {1} MB".format(PythonTest.to_mb(mem_topo.tom()), PythonTest.to_mb(mem_topo.tom2()))
dram_hole = mem_topo.dramHole()
print "DRAM HOLE = {0} MB to {1} MB ".format(dram_hole.baseMB(), dram_hole.limitMB())

for node in mem_topo.nodes():
  print "Node {0} with DCT Interleaving = {1}".format(node.physicalID(), node.dctInterleaved())
  for dct in node.dcts():
    print "\tDCT {0}".format(dct.physicalID())


