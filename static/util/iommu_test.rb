### This test script is created as an example, may use this script as a sanity in the future, thus Test Suite folder will have an additional folder "Test" which will include this
require 'C:\Program Files (x86)\AMD\Kysy\Ruby\Kysy'
require '.\..\..\lib\Kysy_Wrapper\KysyWrapper'
#require '.\..\..\lib\Common\COMMON'
#require '.\..\..\lib\Products\dGPU\DGPU'
#require '.\..\..\lib\IP\core\cpu_core'
#require '.\..\..\lib\IP\NBIF\nbif_ver1_X'

def debug_Step()
	puts "type and enter on CMD to continue"
	temp = gets
end

### LOOK AT THIS
def memAccessTest(test_kysyWrapper_Inst)
	### test to read write using memory access (platform object, read/write, base addr, data to write (0 if read), size in bytes)
	test = test_kysyWrapper_Inst.kysyWrapper_MemWr(0x5000_0000, 0xdead_0123_8765_BEEF, 4)
	test = test_kysyWrapper_Inst.kysyWrapper_MemDeAssert(0x5000_0000, 0xA, 1)
	test = test_kysyWrapper_Inst.kysyWrapper_MemRd(0x5000_0000, 1)
	print "value read: #{test.to_s(16)}\n"
end

def memFillTest(test_kysyWrapper_Inst)
	### test to read write using memory access (platform object, read/write, base addr, data to write (0 if read), size in bytes)
	test = test_kysyWrapper_Inst.kysyWrapper_MemWr(0x5000_0000, 0x0, 4)
	test = test_kysyWrapper_Inst.kysyWrapper_MemWr(0x5000_0000, 0x0, 4)
	test = test_kysyWrapper_Inst.kysyWrapper_MemWr(0x5000_0000, 0x0, 4)
	test = test_kysyWrapper_Inst.kysyWrapper_MemWr(0x5000_0000, 0x0, 4)
	
	testDataArray = [0xdead1, 0xdead2, 0xdead3, 0xdead4]
	testDataBytes = (testDataArray.length*4).to_i
	
	test = test_kysyWrapper_Inst.kysyWrapper_MemFill_Dword(0x5000_0000, testDataArray, testDataBytes)

	test = test_kysyWrapper_Inst.kysyWrapper_MemRd(0x5000_0000, 4)
	puts "value read #{test.to_s(16)}"
	test = test_kysyWrapper_Inst.kysyWrapper_MemRd(0x5000_0004, 4)
	puts "value read #{test.to_s(16)}"
	test = test_kysyWrapper_Inst.kysyWrapper_MemRd(0x5000_0008, 4)
	puts "value read #{test.to_s(16)}"
	test = test_kysyWrapper_Inst.kysyWrapper_MemRd(0x5000_000C, 4)
	puts "value read #{test.to_s(16)}"
end

### LOOK AT THIS
def register_by_path_test(test_kysyWrapper_Inst)
	### test using read by path (platform object, read/write, path, data to write (0 if read), size in bytes)
	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", "COM_BASE_LO", 'MEM')
	print "value read: #{test.to_s(16)}\n"

	test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", "COM_BASE_LO", 0xA_A55F, 'SMN')

	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", "COM_BASE_LO", 'MEM')
	print "value read after write: #{test.to_s(16)}\n"
	
	test = test_kysyWrapper_Inst.kysyWrapper_regDeAssertByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", "COM_BASE_LO", 0x8_844A, 'SMN')
	
	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", "COM_BASE_LO", 'MEM')
	print "value read after deAssert: #{test.to_s(16)}\n"
	
	test = test_kysyWrapper_Inst.kysyWrapper_regAssertByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", "COM_BASE_LO", 0x1_1220, 'SMN')
	
	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", "COM_BASE_LO", 'MEM')
	print "value read after Assert: #{test.to_s(16)}\n"
	
	test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", nil, 0x0, 'SMN')
	
	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CMD_BASE_0", nil, 'MEM')
	print "value read after Assert: #{test.to_s(16)}\n"

end

### LOOK AT THIS
def register_PPRSetFields_test(test_kysyWrapper_Inst)
	### test using read by path (platform object, read/write, path, data to write (0 if read), size in bytes)
	
	#Hash for every value that needs to be bit encoded
	setFields = {"PPR_LOG_EN" => 1, "EVENT_LOG_EN" => 1}
	test = test_kysyWrapper_Inst.kysyWrapper_PPRSetFields("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", 0x400, setFields)
	print "value read: #{test.to_s(16)}\n"

end

def register_by_path_field_test(test_kysyWrapper_Inst)
	### test using read by path (platform object, read/write, path, data to write (0 if read), size in bytes)
	v_test_hash = {"EVENT_LOG_EN"=>0, "CMD_BUF_EN"=>0}
	
	test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", v_test_hash, nil, 'MEM')
	
	v_test_hash = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", v_test_hash, 'MEM')
	v_test_hash.each do |v_key, v_value|
		puts "#{v_key} value read: #{v_value}\n"
	end
	
	v_test_hash["EVENT_LOG_EN"] = 1
	v_test_hash["CMD_BUF_EN"] = 1
	
	test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", v_test_hash, nil, 'MEM')
	
	v_test_hash = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", v_test_hash, 'MEM')
	v_test_hash.each do |v_key, v_value|
		puts "#{v_key} value read: #{v_value}\n"
	end
	
end

def register_by_path_ioapic_test(test_kysyWrapper_Inst)
	### test using read by path (platform object, read/write, path, data to write (0 if read), size in bytes)
	puts "IOAPIC index data test"
	#test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOAPIC::socket0::die0::IOAPICMIO_INDEX", nil, 0x1, 'MEM')

	#test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOAPIC::socket0::die0::IOAPICMIO_DATA", nil, 'MEM')
	
	test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOHC::socket0::die0::IOAPIC_MIO_INDEX", nil, 0x1, 'SMN')
	
	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOHC::socket0::die0::IOAPIC_MIO_INDEX", nil, 'SMN')
	puts test.to_s()
	
	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOHC::socket0::die0::IOAPIC_MIO_DATA", nil, 'SMN')
	
	puts test.to_s()
	puts "end ioapic test"
end

### LOOK AT THIS
def smnAccess_test(test_kysyWrapper_Inst)
	### test using SMN read/write address
	test = test_kysyWrapper_Inst.kysyWrapper_readSmnBuffer(0x1110_4072)
	print "value read: #{test.to_s(16)}\n"
end

### LOOK AT THIS

def cfg_Space_Access_test(test_kysyWrapper_Inst)
	### test to read to config space
	#test = test_kysyWrapper_Inst.kysyWrapper_MemRd(0xFFFE10800000, 4)
	#print "value read: #{test.to_s(16)}\n" 
	test = test_kysyWrapper_Inst.kysyWrapper_MemAssert(0x5000_0000, 0x55, 4)
	test = test_kysyWrapper_Inst.kysyWrapper_CfgSpace_read(0x0, 0x0, 0x2, 0x0)
	print "value read: #{test.to_s(16)}\n"
end

def dGPU_IndirectSpace_Access (test_kysyWrapper_Inst, common_Inst)
	### Read SMCIND in Tonga to test COMMON.indexDataPair_XX_ByMem
	dGPU_busNum = 8
	mmio_Base = test_kysyWrapper_Inst.kysyWrapper_CfgSpace_read(dGPU_busNum, 0x0, 0x0, 0x24)
	index_reg = mmio_Base + 0x220
	data_reg = mmio_Base + 0x224
	scratch_reg_Offset = 0x8000_0400
	
	value = common_Inst.indexDataPair_Wr_ByMem(index_reg, data_reg, scratch_reg_Offset, 0x0)
	print "Written value: #{value}\n"
	
	value = common_Inst.indexDataPair_Rd_ByMem(index_reg, data_reg, scratch_reg_Offset)
	print "value read: #{value.to_s(16)}\n"
	
	value = common_Inst.indexDataPair_Wr_ByMem(index_reg, data_reg, scratch_reg_Offset, 0xDEAD_BEEF)
	print "Written value: #{value}\n"
	
	value = common_Inst.indexDataPair_Rd_ByMem(index_reg, data_reg, scratch_reg_Offset)
	print "value read: #{value.to_s(16)}\n"
end

def host_Translation_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	dGPU_Tonga_Inst.dGPU_SetUp
	
	### Toggle IDO, RO, Snoop bits (if needed)
	#dGPU_Tonga_Inst.dGPU_SetRO
	#dGPU_Tonga_Inst.dGPU_SetIDO
	#dGPU_Tonga_Inst.dGPU_SetSnoop
	#dGPU_Tonga_Inst.dGPU_ClearRO
	#dGPU_Tonga_Inst.dGPU_ClearSnoop
	#dGPU_Tonga_Inst.dGPU_ClearIDO
	
	
	v_sdma0_rb_base_gfx = dGPU_Tonga_Inst.dGPU_FB_LOCATION_BASE.to_i
	v_sdma0_rb_base_cpu = dGPU_Tonga_Inst.dGPU_FrameBufferBAR.to_i

	v_sdma_systemMem = 0x5000_0000
	v_sdma_FB_offset = 0x1000
	
	data = 0x12345
	#data = 0x44455
	#data = 0x33333
	
	# Read Setup MEM
	test_kysyWrapper_Inst.kysyWrapper_MemWr(v_sdma_systemMem, data.to_i, 4)
	test_kysyWrapper_Inst.kysyWrapper_MemWr(v_sdma0_rb_base_cpu + v_sdma_FB_offset, 0, 4)
	
	#Write Setup MEM
	#test_kysyWrapper_Inst.kysyWrapper_MemWr(v_sdma_systemMem, 0, 4)
	#test_kysyWrapper_Inst.kysyWrapper_MemWr(v_sdma0_rb_base_cpu + v_sdma_FB_offset, data.to_i, 4)
	
	# Read Linear copy
	dGPU_Tonga_Inst.dGPU_Setup_SDMA_Linear_Copy_Wrapper(v_sdma0_rb_base_cpu, 0x4, v_sdma_systemMem, v_sdma0_rb_base_gfx + v_sdma_FB_offset)
	
	# Write Linear copy
	#dGPU_Tonga_Inst.dGPU_Setup_SDMA_Linear_Copy_Wrapper(v_sdma0_rb_base_cpu, 0x4, v_sdma0_rb_base_gfx + v_sdma_FB_offset, v_sdma_systemMem)
	
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Enable
		
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Initiate
	test = false
	test = dGPU_Tonga_Inst.dGPU_OSS_SDMA_Check_Finish
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
	
	# Read result
	puts (test_kysyWrapper_Inst.kysyWrapper_MemRd(v_sdma0_rb_base_cpu + v_sdma_FB_offset, 4)).to_s(16)
	
	# Write result
	#puts (test_kysyWrapper_Inst.kysyWrapper_MemRd(v_sdma_systemMem, 4)).to_s(16)
	return test
	# may need 
end

def host_Translation_ATS_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	result = false
	dGPU_Tonga_Inst.dGPU_SetUp
	v_sdma0_rb_base_gfx = dGPU_Tonga_Inst.dGPU_FB_LOCATION_BASE.to_i
	v_sdma0_rb_base_cpu = dGPU_Tonga_Inst.dGPU_FrameBufferBAR.to_i
	
	v_sdma_destination = 0x5000_0000
	### ATC Aperture should cover the minimum virtual address range for traffic
	### DO NOT OVERLAP with MMIO and other apertures
	dGPU_Tonga_Inst.dGPU_Set_ATC_Aperture(v_sdma_destination, v_sdma_destination + 0x1000_0000)
	dGPU_Tonga_Inst.dGPU_Enable_ATS()
	#dGPU_Tonga_Inst.dGPU_Enable_Guest(0x1, 0x123)
	dGPU_Tonga_Inst.dGPU_Setup_SDMA_Linear_Copy_Wrapper(v_sdma0_rb_base_cpu, 16, v_sdma0_rb_base_gfx, v_sdma_destination)
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Enable
		
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Initiate
	result = dGPU_Tonga_Inst.dGPU_OSS_SDMA_Check_Finish
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
	return result
	# may need dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
end

### NEED TO TEST: Current result, run this function twice will generate 
###				at least one PRI (Assuming ATS is working and setup 
###				in IOMMU) 
###				MAX 4 PRI per run
def host_Translation_ATS_PRI_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	result = false
	dGPU_Tonga_Inst.dGPU_SetUp
	v_sdma0_rb_base_gfx = dGPU_Tonga_Inst.dGPU_FB_LOCATION_BASE.to_i
	v_sdma0_rb_base_cpu = dGPU_Tonga_Inst.dGPU_FrameBufferBAR.to_i
	
	v_sdma_destination = 0x1000
	
	### ATC Aperture should cover the minimum virtual address range for traffic
	### DO NOT OVERLAP with MMIO and other apertures
	dGPU_Tonga_Inst.dGPU_Set_ATC_Aperture(v_sdma_destination, v_sdma_destination + 0x1000_0000)
	dGPU_Tonga_Inst.dGPU_Enable_ATS
	dGPU_Tonga_Inst.dGPU_Enable_PRI
	#dGPU_Tonga_Inst.dGPU_Enable_Guest(0x1, 0x123)
	dGPU_Tonga_Inst.dGPU_Setup_SDMA_Linear_Copy_Wrapper(v_sdma0_rb_base_cpu, 16, v_sdma0_rb_base_gfx, v_sdma_destination)
	#dGPU_Tonga_Inst.dGPU_Setup_SDMA_Linear_Copy_Wrapper(v_sdma0_rb_base_cpu + dGPU_Tonga_Inst.dGPU_OSS_SDMA_Total_Number_Of_Bytes, 16, v_sdma0_rb_base_gfx, v_sdma_destination+0x1000)

	### Test loop (Remove later)
	for i in 1..128
		dGPU_Tonga_Inst.dGPU_Setup_SDMA_Linear_Copy_Wrapper(v_sdma0_rb_base_cpu + dGPU_Tonga_Inst.dGPU_OSS_SDMA_Total_Number_Of_Bytes, 16, v_sdma0_rb_base_gfx, v_sdma_destination+(0x1000*i))
	end
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Enable
		
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Initiate
	result = dGPU_Tonga_Inst.dGPU_OSS_SDMA_Check_Finish
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
	return result
	# may need dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
end

def atomic_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	
	### Things to be done manually on APU/CPU (until PCIE IP Class is created)
	#Manually set the following in HDT (dGPU MUST HAVE ATOMICS ENABLED)
	#PCIE_CORE.PCIE_STRAP_F0 (STRAP_F0_ATOMIC_EN, STRAP_F0_ATOMIC_ROUTING_EN = 1)
	#PCIE_RCCFG.PCIE_DEVICE_CNTL2_LINK0-7 (ATOMICOP_REQUEST_EN = 1) *Per PCIE Core
	dGPU_Tonga_Inst.dGPU_SetUp
	v_sdma0_rb_base_gfx = dGPU_Tonga_Inst.dGPU_FB_LOCATION_BASE.to_i
	v_sdma0_rb_base_cpu = dGPU_Tonga_Inst.dGPU_FrameBufferBAR.to_i
	
	v_sdma_destination = 0x5000_0000
	
	test_kysyWrapper_Inst.kysyWrapper_MemWr(v_sdma_destination, 0x4000, 4)
	dGPU_Tonga_Inst.dGPU_Enable_Atomic
	dGPU_Tonga_Inst.dGPU_Setup_SDMA_Atomic_Wrapper(v_sdma0_rb_base_cpu, 0xF, 0x0, v_sdma_destination, 0x123, 0x0, 0x0)
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Enable
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Initiate
	sleep(3)
	puts test_kysyWrapper_Inst.kysyWrapper_MemRd(v_sdma_destination, 4)
	result = dGPU_Tonga_Inst.dGPU_OSS_SDMA_Check_Finish
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
	return result
	# 
end

def guest_Translation_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	dGPU_Tonga_Inst.dGPU_SetUp
	dGPU_Tonga_Inst.dGPU_SetPMR
	v_sdma0_rb_base_gfx = dGPU_Tonga_Inst.dGPU_FB_LOCATION_BASE.to_i
	v_sdma0_rb_base_cpu = dGPU_Tonga_Inst.dGPU_FrameBufferBAR.to_i
		
	v_sdma_destination = 0x11_5000_0000
	### ATC Aperture should cover the minimum virtual address range for traffic
	### DO NOT OVERLAP with MMIO and other apertures
	dGPU_Tonga_Inst.dGPU_Set_ATC_Aperture(v_sdma_destination, v_sdma_destination + 0x1000_0000)
	dGPU_Tonga_Inst.dGPU_Enable_Guest(0x1, 0x1123)
	dGPU_Tonga_Inst.dGPU_Setup_SDMA_Linear_Copy_Wrapper(v_sdma0_rb_base_cpu, 16, v_sdma0_rb_base_gfx, v_sdma_destination)
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Enable
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Initiate
	result = dGPU_Tonga_Inst.dGPU_OSS_SDMA_Check_Finish
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
	return result
end

### LOOK AT THIS
def read_core_reg_test(test_kysyWrapper_Inst)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_3002, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_3003, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_3004, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_3005, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_3006, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0x0000_0448, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1000, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_100A, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_100E, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_100F, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1014, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1015, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1016, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1017, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1018, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1024, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1025, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1026, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1027, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0x0000_01D9, 0, 0, 0, 0, 0)
	puts test.to_s(16)

	#test = test_kysyWrapper_Inst.kysyWrapper_SPR_Wr(0x448, 0x111111, 0, 0, 0, 0, 0)
	test = test_kysyWrapper_Inst.kysyWrapper_SPR_Rd(0x448, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_SPR_Rd(0x6, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	test = test_kysyWrapper_Inst.kysyWrapper_SPR_Rd(0xC001_1014, 0, 0, 0, 0, 0)
	puts test.to_s(16)
	
	#test = test_kysyWrapper_Inst.kysyWrapper_MSR_Wr(0xC0011014, 0xEEEEEE, 0, 0, 0, 0, 0)
	test = test_kysyWrapper_Inst.kysyWrapper_MSR_Rd(0xC001_1014, 0, 0, 0, 0, 0)
	puts test.to_s(16)
end

### LOOK AT THIS
def platform_cold_reset(test_kysyWrapper_Inst)
	### Set Cold Reboot assuming Relays are connected and it is a WOMBAT
	test_kysyWrapper_Inst.kysyWrapper_ColdReset
end

def interrupt_test_Tonga(test_kysyWrapper_Inst, dGPU_Tonga_Inst, cpu_core_Inst)
	### Test to Setup/send/check Interrupt
	#cpu_core_Inst.core_INTERRUPT_DEBUG_Reset()
	#dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset()
	
	### Use this for MSI interrupts
	dGPU_Tonga_Inst.dGPU_SetUp
	v_sdma0_rb_base_gfx = dGPU_Tonga_Inst.dGPU_FB_LOCATION_BASE.to_i
	v_sdma0_rb_base_cpu = dGPU_Tonga_Inst.dGPU_FrameBufferBAR.to_i
	
	### Use this for INTx Interrupts, make sure corresponding IOAPIC mask is 0
	##########################################################
	### enable only one of these functions
	dGPU_Tonga_Inst.dGPU_Set_MSI(0x0, 0x0, 0x0, 0x0, 0x3D)
	#dGPU_Tonga_Inst.dGPU_Set_LegacyInterrupt()
	##########################################################
	dGPU_Tonga_Inst.dGPU_Enable_OSS_IH(v_sdma0_rb_base_gfx + 0x1000)
	dGPU_Tonga_Inst.dGPU_Setup_SDMA_Trap_Wrapper(v_sdma0_rb_base_cpu, 0x1)
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Enable
	cpu_core_Inst.core_INTERRUPT_DEBUG_Setup(0x3D)
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Initiate
	result = false
	result = cpu_core_Inst.core_INTERRUPT_check_caught
	puts result
	
	cpu_core_Inst.core_INTERRUPT_DEBUG_Reset()
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset()
end

def interrupt_test_nbif(test_kysyWrapper_Inst, nbif_Inst, cpu_core_Inst, msi_chk, msi_addr, msi_data, bus, dev, func, interrupt_test)
	### Test to Setup/send/check Interrupt
	cpu_core_Inst.core_ClearAllInterrupts
	if (interrupt_test == 0)
		cpu_core_Inst.core_INTERRUPT_DEBUG_Setup(msi_data&0xFF)
	else
		cpu_core_Inst.core_INTERRUPT_DEBUG_Setup(0x51&0xFF)
	end
	
	nbif_Inst.sendBridgeInterrupt(msi_chk, msi_addr, msi_data, bus, dev, func)
	
	result = false
	result = cpu_core_Inst.core_INTERRUPT_check_caught
	puts result
	nbif_Inst.clearBridgeInterrupt
	cpu_core_Inst.core_INTERRUPT_DEBUG_Reset()
	return result
	### IOAPIC to add function here to check if recieved in IOAPIC
	### Should check Delivery Status bit in IOAPIC remapping entry
end

def batchPerfTest (test_kysyWrapper_Inst)
	### Change cycle to check performance
	### This is just to compare performance between batch and regular,
	### Need to uncomment the following 2 green lines to compare
	
	cycle = 1
	
	t1 = Time.now.to_f
	for count in 0..cycle
	### uncomment the following 2 lines to test performance of regular reads/writes
		#test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_DEVTBL_BASE_0", nil, 0x0, 'MEM')
		
		#test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_DEVTBL_BASE_0", nil, 'MEM')
	end
	t2 = Time.now.to_f
	delta = t2-t1
	puts "Time delta #{delta} for regular reg read"
	
	reg = [[]]
	data = []
	
	for count in 0..cycle
		reg[2*count] = ["PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_DEVTBL_BASE_0", 'MEM', count*0x1_0000]
		reg[2*count+1] = ["PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_DEVTBL_BASE_0", 'MEM', nil]
	end
	
	t1 = Time.now.to_f
	data = test_kysyWrapper_Inst.kysyWrapper_regAccessByPathBatch(reg)
	t2 = Time.now.to_f
	delta = t2-t1
	puts "Time delta #{delta} for batch reg read"
	
	for value in data
		puts "value in return array #{value.to_s(16)}."
	end
end

def batchOrderingTest (test_kysyWrapper_Inst)
	reg = [[]]
	data = []

	reg[0] = ["PPR::IOHC::socket0::die0::NBCFG_SCRATCH_0", 'SMN', 1]
	reg[1] = ["PPR::IOHC::socket0::die0::NBCFG_SCRATCH_0", 'SMN', nil]
	reg[2] = ["PPR::IOHC::socket0::die0::NBCFG_SCRATCH_0", 'SMN', 2]
	#reg[3] = ["PPR::IOHC::socket0::die0::NBCFG_SCRATCH_0", 'SMN', nil]
	
	data = test_kysyWrapper_Inst.kysyWrapper_regAccessByPathBatch(reg)
	
	puts "results #{data}"
end

def ryan_regByPath_bifStrapAccess (test_kysyWrapper_Inst)
	### TEST FOR ZP
	test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", "EVENT_LOG_EN", 0x1, 'SMN')

	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", "EVENT_LOG_EN", 'SMN')
	puts test
	test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", "EVENT_LOG_EN", 0x1, 'SMN')
	
	test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::IOMMUMMIO::socket0::die0::IOMMU_MMIO_CNTRL_0", "EVENT_LOG_EN", 'SMN')
	#puts test
	
	### TEST FOR RV
	#test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath(	"PPR::NBIFEPFCFG::socket0::die0::AMDGFX::MSI_MSG_CNTL", "MSI_EN", 0x0, 'SMN')
	#test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::NBIFEPFCFG::socket0::die0::AMDGFX::MSI_MSG_CNTL", nil, 'SMN')
	#puts test
	#test = test_kysyWrapper_Inst.kysyWrapper_regWrByPath(	"PPR::NBIFEPFCFG::socket0::die0::AMDGFX::MSI_MSG_CNTL", "MSI_EN", 0x1, 'SMN')
	#test = test_kysyWrapper_Inst.kysyWrapper_regRdByPath("PPR::NBIFEPFCFG::socket0::die0::AMDGFX::MSI_MSG_CNTL", nil, 'SMN')
	#puts test
end

def dgpu_Write (test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	v_DMA_WrAddr = 0x5000_0000
	v_DMA_WrData = []
	v_DMA_SizeInBytes = 0x8 ## Must be a multiple of 4
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		v_DMA_WrData[i] = 0x29+i
	end
	
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		(test_kysyWrapper_Inst.kysyWrapper_MemWr(v_DMA_WrAddr + i*4, 0, 4))
	end
	
	dGPU_Tonga_Inst.dGPU_DMA_Write(v_DMA_WrAddr, v_DMA_SizeInBytes, v_DMA_WrData, nil, nil)
	
	puts "Data read back:"
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		puts "	Read value #{(test_kysyWrapper_Inst.kysyWrapper_MemRd(v_DMA_WrAddr + i*4, 4)).to_s(16)}"
	end
	puts "read end"
end

def dgpu_Read (test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	v_DMA_RdAddr = 0x5000_0000
	v_Data = 0x5
	v_DMA_SizeInBytes = 8 ### Must be a multiple of 4
	
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		test_kysyWrapper_Inst.kysyWrapper_MemWr(v_DMA_RdAddr + i*4, (v_Data + i), 4)
	end
	
	v_read_value = dGPU_Tonga_Inst.dGPU_DMA_Read(v_DMA_RdAddr, v_DMA_SizeInBytes, nil, nil)

	#puts "Read value #{v_read_value}"
	puts "Data read back:"
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		puts "	Read value #{v_read_value[i].to_s(16)}"
	end
	puts "read end"
end

def dgpu_Guest_Read (test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	v_DMA_RdAddr = 0x5000_0000
	v_Data = 0x5
	v_DMA_SizeInBytes = 4 ### Must be a multiple of 4
	v_PASID = 0x123
	
	v_guest = dGPU_Tonga_Inst.dGPU_guest_Struct.new(v_PASID, nil, nil, nil)
	
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		test_kysyWrapper_Inst.kysyWrapper_MemWr(v_DMA_RdAddr + i*4, (v_Data + i), 4)
	end
	
	v_read_value = dGPU_Tonga_Inst.dGPU_DMA_Read(v_DMA_RdAddr, v_DMA_SizeInBytes, nil, v_guest)

	#puts "Read value #{v_read_value}"
	puts "Data read back:"
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		puts "	Read value #{v_read_value[i].to_s(16)}"
	end
	puts "read end"
end

def dgpu_Guest_Write (test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	v_DMA_WrAddr = 0x5000_0000
	v_DMA_WrData = []
	v_DMA_SizeInBytes = 0x8 ## Must be a multiple of 4
	v_PASID = 0x123
	
	v_guest = dGPU_Tonga_Inst.dGPU_guest_Struct.new(v_PASID, nil, nil, nil)
	
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		v_DMA_WrData[i] = 0x29+i
	end
	
	dGPU_Tonga_Inst.dGPU_DMA_Write(v_DMA_WrAddr, v_DMA_SizeInBytes, v_DMA_WrData, nil, v_guest)
	
	puts "Data read back:"
	for i in 0..(v_DMA_SizeInBytes/4 -1)
		puts "	Read value #{(test_kysyWrapper_Inst.kysyWrapper_MemRd(v_DMA_WrAddr + i*4, 4)).to_s(16)}"
	end
	puts "read end"
end

def dgpu_Tonga_INTx (dGPU_Tonga_Inst)
	dGPU_Tonga_Inst.dGPU_INTx
end

def dgpu_Tonga_MSI (test_kysyWrapper_Inst, dGPU_Tonga_Inst, cpu_core_Inst)
	### Test to Setup/send/check Interrupt
	#cpu_core_Inst.core_INTERRUPT_DEBUG_Reset()
	#dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset()
	v_vector = 0x3d
	v_destination = 0x0
	v_destination_Mode = 0x0
	v_trigger_mode = 0x0
	v_level_trigger_mode = 0x0
	v_delivery_mode = 0x0
	cpu_core_Inst.core_INTERRUPT_DEBUG_Setup(v_vector)
	
	v_msi_addr = dGPU_Tonga_Inst.dGPU_msi_Addr_struct.new(v_destination, v_destination_Mode)
	v_msi_data = dGPU_Tonga_Inst.dGPU_msi_Data_struct.new(v_trigger_mode, v_level_trigger_mode, v_delivery_mode, v_vector)
	dGPU_Tonga_Inst.dGPU_send_MSI(v_msi_addr, v_msi_data)
	
	result = false
	result = cpu_core_Inst.core_INTERRUPT_check_caught
	puts "interrupt caught at core: #{result}"
	
	cpu_core_Inst.core_INTERRUPT_DEBUG_Reset()
	dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset()
end

def dGPU_Tonga_ATS_read(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	result = false
	v_ATS_Addr = 0x8000_0000
	dGPU_Tonga_Inst.dGPU_SetUp
	result = dGPU_Tonga_Inst.dGPU_send_ATS_read(v_ATS_Addr, nil, nil)
	puts "ATS sent: #{result}"
	return result
	# may need dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
end

def dGPU_Tonga_ATS_write(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	result = false
	v_ATS_Addr = 0x8000_0000
	dGPU_Tonga_Inst.dGPU_SetUp
	result = dGPU_Tonga_Inst.dGPU_send_ATS_write(v_ATS_Addr, nil, nil)
	puts "ATS sent: #{result}"
	return result
	# may need dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
end

def dGPU_Tonga_PRI(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	result = false
	v_PRI_Addr = 0x5000_0000
	dGPU_Tonga_Inst.dGPU_SetUp
	result = dGPU_Tonga_Inst.dGPU_send_PRI(v_PRI_Addr, nil, nil)
	puts "ATS sent: #{result}"
	return result
	# may need dGPU_Tonga_Inst.dGPU_OSS_SDMA_Reset
end

def dGPU_atomic_FetchAdd(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	
	### Things to be done manually on APU/CPU (until PCIE IP Class is created)
	#Manually set the following in HDT (dGPU MUST HAVE ATOMICS ENABLED)
	#PCIE_CORE.PCIE_STRAP_F0 (STRAP_F0_ATOMIC_EN, STRAP_F0_ATOMIC_ROUTING_EN = 1)
	#PCIE_RCCFG.PCIE_DEVICE_CNTL2_LINK0-7 (ATOMICOP_REQUEST_EN = 1) *Per PCIE Core
	v_sdma_destination = 0x5000_0000
	v_FetchAdd_Data = 0x123
	v_destination_Data = 0x3
	test_kysyWrapper_Inst.kysyWrapper_MemWr(v_sdma_destination, v_destination_Data, 4)
	
	result = dGPU_Tonga_Inst.dGPU_send_Atomic_FetchAdd(v_sdma_destination, v_FetchAdd_Data)
	
	puts "SDMA result #{result}, original: #{v_destination_Data.to_s(16)}, added: #{v_FetchAdd_Data.to_s(16)}, resulting value: #{(test_kysyWrapper_Inst.kysyWrapper_MemRd(v_sdma_destination, 4)).to_s(16)}"

	return result
end

def dGPU_atomic_Swap(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	### examples for accessing DGPU class, and DGPU_MMIO/DGPU_CFG_Space
	
	### Things to be done manually on APU/CPU (until PCIE IP Class is created)
	#Manually set the following in HDT (dGPU MUST HAVE ATOMICS ENABLED)
	#PCIE_CORE.PCIE_STRAP_F0 (STRAP_F0_ATOMIC_EN, STRAP_F0_ATOMIC_ROUTING_EN = 1)
	#PCIE_RCCFG.PCIE_DEVICE_CNTL2_LINK0-7 (ATOMICOP_REQUEST_EN = 1) *Per PCIE Core
	v_sdma_destination = 0x5000_0000
	v_FetchAdd_Data = 0x123
	v_destination_Data = 0x3
	test_kysyWrapper_Inst.kysyWrapper_MemWr(v_sdma_destination, v_destination_Data, 4)
	
	result = dGPU_Tonga_Inst.dGPU_send_Atomic_Swap(v_sdma_destination, v_FetchAdd_Data)
	
	puts "SDMA result #{result.to_s(16)}, destination: #{(test_kysyWrapper_Inst.kysyWrapper_MemRd(v_sdma_destination, 4)).to_s(16)}"

	return result
end

def sandbox (test_kysyWrapper_Inst, cpu_core_Inst)
	cpu_core_Inst.core_ClearAllInterrupts
	cpu_core_Inst.core_INTERRUPT_DEBUG_Setup(0x1)
	#debug_Step()
	
	result = false
	result = cpu_core_Inst.core_INTERRUPT_check_caught
	puts result
	#nbif_Inst.clearBridgeInterrupt
	cpu_core_Inst.core_INTERRUPT_DEBUG_Reset()
	return result
end

def iommu_Main () 
	###THINGS TO DO
	###Separate nbif interrupt send to assert int and deassert int
	test_kysyWrapper_Inst = KysyWrapper.new
	common_Inst = COMMON.new(test_kysyWrapper_Inst)
	dGPU_Tonga_Inst = DGPU.new(test_kysyWrapper_Inst, common_Inst, 0x8, 0x0, 0x0)
	cpu_core_Inst = CPU_CORE.new(test_kysyWrapper_Inst, "PPR::Core::X86::Apic::socket0::die0::lthree0::core0::thread0::")
	nbif_Inst = NBIF_ver1_X.new(test_kysyWrapper_Inst, "PPR::NBIFRCCFG::socket0::die0::NBIF0::", "PPR::NBIFMM::socket0::die0::NBIF0::", "ZP")
	test = ""
	###################################################################################
	###Set Platform from WOMBAT
	###################################################################################
	test_kysyWrapper_Inst.kysyWrapper_setup("10.1.35.1","daoli","password")

	###################################################################################
	###Set PDM mode
	###################################################################################
	puts "PDM Status: #{test_kysyWrapper_Inst.kysyWrapper_SET_PDM()}"
	###################################################################################
	
	### KysyWrapper Test 
	### 1) Memory Access test
	#memAccessTest(test_kysyWrapper_Inst)
	
	### 2) Memory Fill 
	#memFillTest(test_kysyWrapper_Inst)
	
	### 3) Register by path test for IOAPIC
	#register_by_path_ioapic_test(test_kysyWrapper_Inst)
	
	### 4) register by path general test
	#register_by_path_test(test_kysyWrapper_Inst)
	
	### 5) dGPU index/data pair test access
	#dGPU_IndirectSpace_Access(test_kysyWrapper_Inst, common_Inst)
	
	### 6) SMN access test
	#smnAccess_test(test_kysyWrapper_Inst)
	
	### 7) configuration space access test
	#cfg_Space_Access_test(test_kysyWrapper_Inst)
	
	### 8) Regular DMA test
	#puts host_Translation_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	
	### 9) ATS DMA test
	#puts "result of sdma check: #{host_Translation_ATS_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)}"
	
	### 10) Atomics DMA test (FetchAdd)
	#atomic_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	
	### 11) Guest Translation Test
	#guest_Translation_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)  
	
	### 12) Core register access test
	#read_core_reg_test(test_kysyWrapper_Inst)
	
	### 13) Platform cold reset test
	#platform_cold_reset(test_kysyWrapper_Inst)
	
	### 14) dGPU Interrupt test
	#interrupt_test_Tonga(test_kysyWrapper_Inst, dGPU_Tonga_Inst, cpu_core_Inst)
	
	### 15) nBIF Bridge Interrupt test
	#result = interrupt_test_nbif(test_kysyWrapper_Inst, nbif_Inst, cpu_core_Inst, 0x1, 0xFEE00000, 0xDD, 0x0, 0x0, 0x0, 0)
	##cpu_core_Inst.core_INTERRUPT_DEBUG_Setup(0xA1)

	### 16) Other batch test
	#batchPerfTest(test_kysyWrapper_Inst)
	
	### 17) Debug Kysy Batch Ordering Test
	#test_kysyWrapper_Inst.test()
	
	### 18) RegByPath Multiple Fields hash Map test
	#register_by_path_field_test(test_kysyWrapper_Inst)
	
	### 19) Register Encoding test
	#register_PPRSetFields_test(test_kysyWrapper_Inst)
	
	### 20) dGPU API Tests:
	#dgpu_Read(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	#dgpu_Write(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	#dgpu_Guest_Read(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	#dgpu_Tonga_INTx(dGPU_Tonga_Inst)
	#dgpu_Tonga_MSI(test_kysyWrapper_Inst, dGPU_Tonga_Inst, cpu_core_Inst)
	#dGPU_Tonga_ATS_read(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	#dGPU_Tonga_ATS_write(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	#dGPU_Tonga_PRI(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	#dGPU_atomic_FetchAdd(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	#dGPU_atomic_Swap(test_kysyWrapper_Inst, dGPU_Tonga_Inst)
	
	### NEED TESTING
	#puts "result of sdma check: #{host_Translation_ATS_PRI_test(test_kysyWrapper_Inst, dGPU_Tonga_Inst)}"
	
	### CUSTOM TESTS
	#ryan_regByPath_bifStrapAccess(test_kysyWrapper_Inst)
	#batchOrderingTest(test_kysyWrapper_Inst)
	#sandbox(test_kysyWrapper_Inst, cpu_core_Inst)
	###################################################################################
	### Exit PDM Mode
	###################################################################################
	#puts "PDM Status: #{test_kysyWrapper_Inst.kysyWrapper_CLEAR_PDM()}"
### FINISH ALL
end
iommu_Main()
print "COMPILE DONE: END ALL\n"