#!/usr/bin/env ruby
require 'C:\Program Files (x86)\AMD\Kysy\Ruby\Kysy'

#####################################################################
### Last Edited Date: 	July 29, 2017
### Last Modified: 		Daoyuan Li
### Version:			0.1
###
### Kysy_RW_IO Class Variables:
###		accessTypes
###		socketID
###		dieID
###		ccxID
###		coreID
###		threadID
###		rw_state (not currently used, should return successful/fail)
###		myWombat
###		kysyWrapper_Platform
###		kysyWrapper_platform_pdm_mode
###		
### KysyWrapper Class Functions: 
###		Initialize
###		kysyWrapper_ResetCoreTopologyPhysicalID
###		kysyWrapper_setup
###		kysyWrapper_SET_PDM
###		kysyWrapper_CLEAR_PDM
###		kysyWrapper_PDM_MODE
###		kysyWrapper_MemRd
###		kysyWrapper_MemWr
###		kysyWrapper_MemAssert
###		kysyWrapper_MemDeAssert
###		kysyWrapper_regRdByPath
###		kysyWrapper_regWrByPath
###		kysyWrapper_regAssertByPath
###		kysyWrapper_regDeAssertByPath
###		kysyWrapper_readSmnBuffer
###		kysyWrapper_writeSmnBuffer
###		kysyWrapper_CfgSpace_read
###		kysyWrapper_CfgSpace_write
###		kysyWrapper_CfgSpace_Assert
###		kysyWrapper_CfgSpace_DeAssert
###		kysyWrapper_ColdReset
###		kysyWrapper_MSRAccess
###		kysyWrapper_SPR_Rd
###		kysyWrapper_SPR_Wr
###		kysyWrapper_MSR_Rd
###		kysyWrapper_MSR_Wr
###
###
#####################################################################
class KysyWrapper

	#Public class variables
	#read-only
	attr_reader :accessTypes
	attr_reader :regByPath_Struct
	attr_reader :regByPath_Commands
	
	#Read and write
	attr_accessor :memory_Access_READ_Types
	attr_accessor :memory_Access_WRITE_Types
	attr_accessor :memory_Destination_Types
	attr_accessor :socketID
	attr_accessor :dieID
	attr_accessor :ccxID
	attr_accessor :coreID
	attr_accessor :threadID
	
	def initialize ()
		#Kysy Memory Access size objects
		@non_default_memory_access_sizes = [Kysy::MEMORY_ACCESS_SIZE_8BIT, Kysy::MEMORY_ACCESS_SIZE_16BIT, Kysy::MEMORY_ACCESS_SIZE_DEFAULT, Kysy::MEMORY_ACCESS_SIZE_32BIT, Kysy::MEMORY_ACCESS_SIZE_DEFAULT, Kysy::MEMORY_ACCESS_SIZE_DEFAULT, Kysy::MEMORY_ACCESS_SIZE_DEFAULT, Kysy::MEMORY_ACCESS_SIZE_64BIT]
		
		#Memory Access types (seems like we cannot use AUTO unless it is native mode)
		@memory_Access_READ_Types = Kysy::MEMORY_TYPE_UNCACHEABLE
		@memory_Access_WRITE_Types = Kysy::MEMORY_TYPE_WRITE_THROUGH 
		@memory_Destination_Types = Kysy::MEMORY_DESTINATION_DRAM
		
		#Core Topology Settings
		@socketID = 0
		@dieID = 0
		@ccxID = 0
		@coreID = 0
		@threadID = 0
		
		#access state
		@rw_state = 0 #doesnt seem to be used for now
		
		#Set Default values
		@myWombat = nil
		@kysyWrapper_Platform = nil
		@kysyWrapper_platform_pdm_mode = 0	
	end
	
	# make this internal function to change as IDs change
	def kysyWrapper_ResetCoreTopologyPhysicalID (a_socketID, a_dieID, a_ccxID, a_coreID, a_threadID)
		@socketID = a_socketID
		@dieID = a_dieID
		@ccxID = a_ccxID
		@coreID = a_coreID
		@threadID = a_threadID
		
		@pprCoreTopoIDs = Kysy::PPRCoreTopologyPhysicalIDs.new(@socketID, @dieID, @ccxID, @coreID, @threadID)
	end
	
	def kysyWrapper_setup (a_kysyWrapper_setup_IP, a_kysyWrapper_setup_Username, a_kysyWrapper_setup_Password)		
		@myWombat = Kysy::Wombat.create(a_kysyWrapper_setup_IP.to_s, a_kysyWrapper_setup_Username.to_s,a_kysyWrapper_setup_Password.to_s)
		
		@kysyWrapper_Platform = @myWombat.platform
		
		#PPR Core Topology ID (access by core)
		@pprCoreTopoIDs = Kysy::PPRCoreTopologyPhysicalIDs.new(@socketID, @dieID, @ccxID, @coreID, @threadID)
	end
	
	def kysyWrapper_Chk_PDM ()
		v_IF_DBRDY = kysyWrapper_regRdByPath("StimGen::Socket0.DIE0.SCF_DFT.DFX.dfx_dft_t.bp_if.BP_IF_DBRDY", nil, 'DFT Broadcast')
		if ((v_IF_DBRDY & 1) == 1)
			@kysyWrapper_platform_pdm_mode = TRUE
		else
			@kysyWrapper_platform_pdm_mode = FALSE
		end
		return @kysyWrapper_platform_pdm_mode
	end
	
	def kysyWrapper_SET_PDM ()
		### Original method to set PDM
		#@myWombat.cpuDebug.requestDebug
		1.upto(3) do
			@myWombat.userPins().dbReq(TRUE)
			sleep(0.1)
			@myWombat.userPins().dbReq(FALSE)
			sleep(0.1)
		end	
		return kysyWrapper_Chk_PDM()
	end
	
	def kysyWrapper_CLEAR_PDM ()
		@myWombat.cpuDebug.exitDebug	
		return kysyWrapper_Chk_PDM()
	end
	
	def kysyWrapper_PDM_MODE ()
		return @kysyWrapper_platform_pdm_mode
	end

	def kysyWrapper_MemRd (a_kysyWrapper_MemRd_Addr, a_kysyWrapper_MemRd_sizeInBytes)
		v_access_size = @non_default_memory_access_sizes[a_kysyWrapper_MemRd_sizeInBytes-1]
		v_bytes = Kysy::Bytes.new(a_kysyWrapper_MemRd_sizeInBytes) # memory size is not hex value, it should be this bytes object
		v_mem = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs, a_kysyWrapper_MemRd_Addr,v_bytes, @memory_Destination_Types, @memory_Access_READ_Types, v_access_size)
			
		v_hexConversion = nil
		
		v_mem.read
		case a_kysyWrapper_MemRd_sizeInBytes
		when 1
			v_kysyWrapper_MemRd_Data = v_mem.byte(0)
		when 2
			v_kysyWrapper_MemRd_Data = v_mem.word(0)
		when 4
			v_kysyWrapper_MemRd_Data = v_mem.dword(0)
		when 8
			v_kysyWrapper_MemRd_Data = v_mem.qword(0)
		else
			v_kysyWrapper_MemRd_Data = v_mem.byte(0)
		end

		return v_kysyWrapper_MemRd_Data.to_i();
	end
	
	def kysyWrapper_MemWr (a_kysyWrapper_MemWr_Addr, a_kysyWrapper_MemWr_Data, a_kysyWrapper_MemWr_sizeInBytes)
		v_access_size = @non_default_memory_access_sizes[a_kysyWrapper_MemWr_sizeInBytes-1]
		v_bytes = Kysy::Bytes.new(a_kysyWrapper_MemWr_sizeInBytes) # memory size is not hex value, it should be this bytes object
		v_mem = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs,a_kysyWrapper_MemWr_Addr,v_bytes, @memory_Destination_Types, @memory_Access_WRITE_Types, v_access_size)
		
		v_hexConversion = nil
		a_kysyWrapper_MemWr_Data = a_kysyWrapper_MemWr_Data & ((1 << (a_kysyWrapper_MemWr_sizeInBytes*8)) - 1)

		case a_kysyWrapper_MemWr_sizeInBytes
		when 1
			v_mem.byte(0,a_kysyWrapper_MemWr_Data.to_i)
		when 2
			v_mem.word(0,a_kysyWrapper_MemWr_Data.to_i)
		when 4
			v_mem.dword(0,a_kysyWrapper_MemWr_Data.to_i)
		when 8
			v_mem.qword(0,a_kysyWrapper_MemWr_Data.to_i)
		else
			v_mem.byte(0,a_kysyWrapper_MemWr_Data.to_i)
		end
		v_mem.write
	end
	
	def kysyWrapper_MemAssert (a_kysyWrapper_MemAssert_Addr, a_kysyWrapper_MemAssert_Data, a_kysyWrapper_MemAssert_sizeInBytes)
		v_access_size = @non_default_memory_access_sizes[a_kysyWrapper_MemAssert_sizeInBytes-1]
		v_bytes = Kysy::Bytes.new(a_kysyWrapper_MemAssert_sizeInBytes) # memory size is not hex value, it should be this bytes object
		v_mem_rd = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs,a_kysyWrapper_MemAssert_Addr,v_bytes, @memory_Destination_Types, @memory_Access_READ_Types, v_access_size)
		
		v_mem_wr = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs,a_kysyWrapper_MemAssert_Addr,v_bytes, @memory_Destination_Types, @memory_Access_WRITE_Types, v_access_size)
		
		v_hexConversion = nil
		a_kysyWrapper_MemAssert_Data = a_kysyWrapper_MemAssert_Data & ((1 << (a_kysyWrapper_MemAssert_sizeInBytes*8)) - 1)
		v_mem_rd.read
		case a_kysyWrapper_MemAssert_sizeInBytes
		when 1
			a_kysyWrapper_MemAssert_Data = a_kysyWrapper_MemAssert_Data.to_i | v_mem_rd.byte(0)
			v_mem_wr.byte(0,a_kysyWrapper_MemAssert_Data.to_i)
		when 2
			a_kysyWrapper_MemAssert_Data = a_kysyWrapper_MemAssert_Data.to_i | v_mem_rd.word(0)
			v_mem_wr.word(0,a_kysyWrapper_MemAssert_Data.to_i)
		when 4
			a_kysyWrapper_MemAssert_Data = a_kysyWrapper_MemAssert_Data.to_i | v_mem_rd.dword(0)
			v_mem_wr.dword(0,a_kysyWrapper_MemAssert_Data.to_i)
		when 8
			a_kysyWrapper_MemAssert_Data = a_kysyWrapper_MemAssert_Data.to_i | v_mem_rd.qword(0)
			v_mem_wr.qword(0,a_kysyWrapper_MemAssert_Data.to_i)
		else
			a_kysyWrapper_MemAssert_Data = a_kysyWrapper_MemAssert_Data.to_i | v_mem_rd.byte(0)
			v_mem_wr.byte(0,a_kysyWrapper_MemAssert_Data.to_i)
		end
		v_mem_wr.write
	end
	
	def kysyWrapper_MemDeAssert (a_kysyWrapper_MemDeAssert_Addr, a_kysyWrapper_DeAssert_Data, a_kysyWrapper_DeAssert_sizeInBytes)
		v_access_size = @non_default_memory_access_sizes[a_kysyWrapper_DeAssert_sizeInBytes-1]
		v_bytes = Kysy::Bytes.new(a_kysyWrapper_DeAssert_sizeInBytes) # memory size is not hex value, it should be this bytes object
		v_mem_rd = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs,a_kysyWrapper_MemDeAssert_Addr,v_bytes, @memory_Destination_Types, @memory_Access_READ_Types, v_access_size)
		
		v_mem_wr = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs,a_kysyWrapper_MemDeAssert_Addr,v_bytes, @memory_Destination_Types, @memory_Access_WRITE_Types, v_access_size)
		
		v_hexConversion = nil
		a_kysyWrapper_DeAssert_Data = a_kysyWrapper_DeAssert_Data & ((1 << (a_kysyWrapper_DeAssert_sizeInBytes*8)) - 1)
		v_mem_rd.read
		case a_kysyWrapper_DeAssert_sizeInBytes
		when 1
			a_kysyWrapper_DeAssert_Data = ~(a_kysyWrapper_DeAssert_Data.to_i) & v_mem_rd.byte(0)
			v_mem_wr.byte(0,a_kysyWrapper_DeAssert_Data.to_i)
		when 2
			a_kysyWrapper_DeAssert_Data = ~(a_kysyWrapper_DeAssert_Data.to_i) & v_mem_rd.word(0)
			v_mem_wr.word(0,a_kysyWrapper_DeAssert_Data.to_i)
		when 4
			a_kysyWrapper_DeAssert_Data = ~(a_kysyWrapper_DeAssert_Data.to_i) & v_mem_rd.dword(0)
			v_mem_wr.dword(0,a_kysyWrapper_DeAssert_Data.to_i)
		when 8
			a_kysyWrapper_DeAssert_Data = ~(a_kysyWrapper_DeAssert_Data.to_i) & v_mem_rd.qword(0)
			v_mem_wr.qword(0,a_kysyWrapper_DeAssert_Data.to_i)
		else
			a_kysyWrapper_DeAssert_Data = ~(a_kysyWrapper_DeAssert_Data.to_i) & v_mem_rd.byte(0)
			v_mem_wr.byte(0,a_kysyWrapper_DeAssert_Data.to_i)
		end
		v_mem_wr.write
	end
	
	def kysyWrapper_regRdByPath (a_regRd_ByPath_regPath, a_regRd_byPath_regField, a_regRd_ByPath_AccessTypes)
		v_register_obj = @kysyWrapper_Platform.regByPath("#{a_regRd_ByPath_regPath}")
		v_logics = v_register_obj.accessLogics
		#print "access v_logics #{v_logics}\n"
		v_acclogic_used = nil

		v_acclogic_check = v_logics.find { |al| al.name =~ /#{a_regRd_ByPath_AccessTypes.to_s}/}
		v_acclogic_used = v_register_obj.accessLogic(a_regRd_ByPath_AccessTypes.to_s)
			
		v_regRd_ByPath_regData = nil
		if (v_acclogic_used != nil)
			v_register_obj.read(v_acclogic_used)
			if (a_regRd_byPath_regField != nil)
				if (a_regRd_byPath_regField.class != Hash)
					v_regRd_ByPath_regData = v_register_obj.field(a_regRd_byPath_regField.to_s).value()
					#puts "field test: #{v_register_obj.field(a_regRd_byPath_regField.to_s).definition()}"
				else
					v_regRd_ByPath_regData = a_regRd_byPath_regField
					a_regRd_byPath_regField.each do |v_key, v_value|
						v_regRd_ByPath_regData["#{v_key}"] = v_register_obj.field("#{v_key}").value()
					end
				end
			else
				v_regRd_ByPath_regData = v_register_obj.value()
			end
		end
		
		return v_regRd_ByPath_regData
	end
	
	def kysyWrapper_regWrByPath (a_regWr_ByPath_regPath, a_regWr_byPath_regField, a_regWr_ByPath_regData, a_regWr_ByPath_AccessTypes)
		v_register_obj = @kysyWrapper_Platform.regByPath("#{a_regWr_ByPath_regPath}")
		v_logics = v_register_obj.accessLogics
		#print "access v_logics #{v_logics}\n"
		v_acclogic_used = nil

		v_acclogic_check = v_logics.find { |al| al.name =~ /#{a_regWr_ByPath_AccessTypes.to_s}/}
		v_acclogic_used = v_register_obj.accessLogic(a_regWr_ByPath_AccessTypes.to_s)
		
		#Writes seem to need to initialize buffer before writing partial values
		if (v_register_obj.accessRight != RegisterDef::ACCESSRIGHT_WO)
			v_register_obj.read(v_acclogic_used)
		end
		if (v_acclogic_used != nil)
			#v_register_obj.read(v_acclogic_used)
			if (a_regWr_byPath_regField != nil)
				if (a_regWr_byPath_regField.class != Hash)
					v_register_obj.field(a_regWr_byPath_regField.to_s).value(a_regWr_ByPath_regData)
				else
					a_regWr_byPath_regField.each do |v_key, v_value|
						v_register_obj.field("#{v_key}").value(v_value)
					end
				end
			else
				v_register_obj.value(a_regWr_ByPath_regData)
			end 
			v_register_obj.write(v_acclogic_used)
		end
	end
	
	def kysyWrapper_regAssertByPath (a_regAssert_ByPath_regPath, a_regAssert_byPath_regField, a_regAssert_ByPath_regData, a_regAssert_ByPath_AccessTypes)
		v_register_obj = @kysyWrapper_Platform.regByPath("#{a_regAssert_ByPath_regPath}")
		v_logics = v_register_obj.accessLogics
		#print "access v_logics #{v_logics}\n"
		v_acclogic_used = nil
		
		v_acclogic_check = v_logics.find { |al| al.name =~ /#{a_regAssert_ByPath_AccessTypes.to_s}/}
		v_acclogic_used = v_register_obj.accessLogic(a_regAssert_ByPath_AccessTypes.to_s)
		
		if (v_acclogic_used != nil)
			if (v_register_obj.accessRight != RegisterDef::ACCESSRIGHT_WO)
				v_register_obj.read(v_acclogic_used)
			end
			if (a_regAssert_byPath_regField != nil)
				a_regAssert_ByPath_regData = a_regAssert_ByPath_regData.to_i | v_register_obj.field(a_regAssert_byPath_regField.to_s).value()
				v_register_obj.field(a_regAssert_byPath_regField.to_s).value(a_regAssert_ByPath_regData)
			else
				a_regAssert_ByPath_regData = a_regAssert_ByPath_regData.to_i | v_register_obj.value()
				v_register_obj.value(a_regAssert_ByPath_regData)
			end
			v_register_obj.write(v_acclogic_used)
		end
	end
	
	def kysyWrapper_regDeAssertByPath (a_regDeAssert_ByPath_regPath, a_regDeAssert_byPath_regField, a_regDeAssert_ByPath_regData, a_regDeAssert_ByPath_AccessTypes)
		v_register_obj = @kysyWrapper_Platform.regByPath("#{a_regDeAssert_ByPath_regPath}")
		v_logics = v_register_obj.accessLogics
		#print "access v_logics #{v_logics}\n"
		v_acclogic_used = nil
		
		v_acclogic_check = v_logics.find { |al| al.name =~ /#{a_regDeAssert_ByPath_AccessTypes.to_s}/}
		v_acclogic_used = v_register_obj.accessLogic(a_regDeAssert_ByPath_AccessTypes.to_s)

		
		if (v_acclogic_used != nil)
			if (v_register_obj.accessRight != RegisterDef::ACCESSRIGHT_WO)
				v_register_obj.read(v_acclogic_used)
			end
			if (a_regDeAssert_byPath_regField != nil)
				
				a_regDeAssert_ByPath_regData = ~(a_regDeAssert_ByPath_regData.to_i) & v_register_obj.field(a_regDeAssert_byPath_regField.to_s).value()
				v_register_obj.field(a_regDeAssert_byPath_regField.to_s).value(a_regDeAssert_ByPath_regData)
			else
				a_regDeAssert_ByPath_regData = ~(a_regDeAssert_ByPath_regData.to_i) & v_register_obj.value()
				v_register_obj.value(a_regDeAssert_ByPath_regData)
			end
			
			v_register_obj.write(v_acclogic_used)
		end
	end

	def kysyWrapper_PPRSetFields (a_Rd_PPRSetFields_regPath, a_PPRSetFields_BaseValue, a_Rd_PPRSetFields_regField, a_Rd_PPRSetFields_AccessTypes = "SMN")
		v_register_obj = @kysyWrapper_Platform.regByPath("#{a_Rd_PPRSetFields_regPath}")
		v_logics = v_register_obj.accessLogics
		#print "access v_logics #{v_logics}\n"
		v_acclogic_used = nil

		v_acclogic_check = v_logics.find { |al| al.name =~ /#{a_Rd_PPRSetFields_AccessTypes.to_s}/}
		v_acclogic_used = v_register_obj.accessLogic(a_Rd_PPRSetFields_AccessTypes.to_s)
		
		v_regRd_ByPath_regData = nil
		if (v_acclogic_used != nil)
			v_register_obj.read(v_acclogic_used)
			v_register_obj.value(a_PPRSetFields_BaseValue)
			
			if (a_Rd_PPRSetFields_regField != nil)
				a_Rd_PPRSetFields_regField.each do |v_key, v_value|
					v_register_obj.field("#{v_key}").value(v_value)
				end
			end 
			v_regRd_ByPath_regData = v_register_obj.value()
		end
		
		return v_regRd_ByPath_regData
	end
	
	def kysyWrapper_readSmnBuffer(a_kysyWrapper_readSmnBuffer_address, a_kysyWrapper_readSmnBuffer_sizeInBytes)
		v_register_obj = Kysy::SMNAxiBufferAccess.create(@kysyWrapper_Platform, @socketID, @dieID, a_kysyWrapper_readSmnBuffer_address, 4, 4)
		v_register_obj.read
		v_data = nil
		case a_kysyWrapper_readSmnBuffer_sizeInBytes
		when 1
			v_data = v_register_obj.byte()
		when 2
			v_data = v_register_obj.word()
		when 4
			v_data = v_register_obj.dword()
		when 8
			v_data = v_register_obj.qword()
		else
			v_data = v_register_obj.byte()
		end

		return v_data.to_i
	end

	def kysyWrapper_writeSmnBuffer(a_kysyWrapper_writeSmnBuffer_address, a_kysyWrapper_writeSmnBuffer_data,  a_kysyWrapper_writeSmnBuffer_sizeInBytes)
		v_register_obj = Kysy::SMNAxiBufferAccess.create(@kysyWrapper_Platform, @socketID, @dieID, a_kysyWrapper_writeSmnBuffer_address, 4, 4)
		case a_kysyWrapper_writeSmnBuffer_sizeInBytes
		when 1
			v_data = v_register_obj.byte(0, a_kysyWrapper_writeSmnBuffer_data)
		when 2
			v_data = v_register_obj.word(0, a_kysyWrapper_writeSmnBuffer_data)
		when 4
			v_data = v_register_obj.dword(0, a_kysyWrapper_writeSmnBuffer_data)
		when 8
			v_data = v_register_obj.qword(0, a_kysyWrapper_writeSmnBuffer_data)
		else
			v_data = v_register_obj.byte(0, a_kysyWrapper_writeSmnBuffer_data)
		end
		v_register_obj.write
	end
	
	def kysyWrapper_CfgSpace_read(a_kysyWrapper_CfgSpace_read_Bus, a_kysyWrapper_CfgSpace_read_Device, a_kysyWrapper_CfgSpace_read_Function, a_kysyWrapper_CfgSpace_read_Offset)
		v_cfgSpace_obj = Kysy::PCIRegister.create(@kysyWrapper_Platform.platformAccess(), a_kysyWrapper_CfgSpace_read_Bus, a_kysyWrapper_CfgSpace_read_Device, a_kysyWrapper_CfgSpace_read_Function, a_kysyWrapper_CfgSpace_read_Offset)
		v_cfgSpace_obj.read
		return (v_cfgSpace_obj.value()).to_i()
	end
	
	def kysyWrapper_CfgSpace_write(a_kysyWrapper_CfgSpace_write_Bus, a_kysyWrapper_CfgSpace_write_Device, a_kysyWrapper_CfgSpace_write_Function, a_kysyWrapper_CfgSpace_write_Offset, a_kysyWrapper_CfgSpace_write_data)
		v_cfgSpace_obj = Kysy::PCIRegister.create(@kysyWrapper_Platform.platformAccess(), a_kysyWrapper_CfgSpace_write_Bus, a_kysyWrapper_CfgSpace_write_Device, a_kysyWrapper_CfgSpace_write_Function, a_kysyWrapper_CfgSpace_write_Offset)
		v_cfgSpace_obj.value(a_kysyWrapper_CfgSpace_write_data)
		v_cfgSpace_obj.write
	end
	
	def kysyWrapper_CfgSpace_Assert(a_kysyWrapper_CfgSpace_Assert_Bus, a_kysyWrapper_CfgSpace_Assert_Device, a_kysyWrapper_CfgSpace_Assert_Function, a_kysyWrapper_CfgSpace_Assert_Offset, a_kysyWrapper_CfgSpace_Assert_data)
		v_cfgSpace_obj = Kysy::PCIRegister.create(@kysyWrapper_Platform.platformAccess(), a_kysyWrapper_CfgSpace_Assert_Bus, a_kysyWrapper_CfgSpace_Assert_Device, a_kysyWrapper_CfgSpace_Assert_Function, a_kysyWrapper_CfgSpace_Assert_Offset)
		v_cfgSpace_obj.read
		a_kysyWrapper_CfgSpace_Assert_data = a_kysyWrapper_CfgSpace_Assert_data.to_i | v_cfgSpace_obj.value()
		v_cfgSpace_obj.value(a_kysyWrapper_CfgSpace_Assert_data)
		v_cfgSpace_obj.write
	end
	
	def kysyWrapper_CfgSpace_DeAssert(a_kysyWrapper_CfgSpace_DeAssert_Bus, a_kysyWrapper_CfgSpace_DeAssert_Device, a_kysyWrapper_CfgSpace_DeAssert_Function, a_kysyWrapper_CfgSpace_DeAssert_Offset, a_kysyWrapper_CfgSpace_DeAssert_data)
		v_cfgSpace_obj = Kysy::PCIRegister.create(@kysyWrapper_Platform.platformAccess(), a_kysyWrapper_CfgSpace_DeAssert_Bus, a_kysyWrapper_CfgSpace_DeAssert_Device, a_kysyWrapper_CfgSpace_DeAssert_Function, a_kysyWrapper_CfgSpace_DeAssert_Offset)
		v_cfgSpace_obj.read
		a_kysyWrapper_CfgSpace_DeAssert_data = ~(a_kysyWrapper_CfgSpace_DeAssert_data.to_i) & v_cfgSpace_obj.value()
		v_cfgSpace_obj.value(a_kysyWrapper_CfgSpace_DeAssert_data)
		v_cfgSpace_obj.write
	end
	
	def kysyWrapper_ColdReset()
		@myWombat.platformPower.execute(Kysy::PlatformPower::COLD_RESET_BUTTON, Kysy::PlatformPower::HOLD)
		sleep 1
		@myWombat.platformPower.execute(Kysy::PlatformPower::COLD_RESET_BUTTON, Kysy::PlatformPower::RELEASE)
	end
	
	def kysyWrapper_SPR_Rd(a_kysyWrapper_SPR_Rd_Addr, a_kysyWrapper_SPR_Rd_socket, a_kysyWrapper_SPR_Rd_die, a_kysyWrapper_SPR_Rd_CCX, a_kysyWrapper_SPR_Rd_Core, kysyWrapper_SPR_Thread=nil)
		v_SPR_pprCoreTopoIDs = Kysy::PPRCoreTopologyPhysicalIDs.new(a_kysyWrapper_SPR_Rd_socket, a_kysyWrapper_SPR_Rd_die, a_kysyWrapper_SPR_Rd_CCX, a_kysyWrapper_SPR_Rd_Core, 0x0)
		
		v_SPR_PDMAPI = Kysy::PDMAccessAPIs.new(@kysyWrapper_Platform.platformAccess())
		v_SPR_Info = Kysy::PDMAccessInfo.new(Kysy::SPECIAL_REG_READ, Kysy::INVALID_PDM_SUB_COMMAND, a_kysyWrapper_SPR_Rd_Addr, 64, 0x0, Kysy::PDMAccessInfo::READ, 4)
		
		v_SPR_PDMAPI.registerMemoryIOAccess(v_SPR_pprCoreTopoIDs, v_SPR_Info)
		
		return v_SPR_Info.readWriteData()
	end
	
	def kysyWrapper_SPR_Wr(a_kysyWrapper_SPR_Wr_Addr, a_kysyWrapper_SPR_Wr_Data, a_kysyWrapper_SPR_Wr_socket, a_kysyWrapper_SPR_Wr_die, a_kysyWrapper_SPR_Wr_CCX, a_kysyWrapper_SPR_Wr_Core, kysyWrapper_SPR_Thread=nil)
		v_SPR_pprCoreTopoIDs = Kysy::PPRCoreTopologyPhysicalIDs.new(a_kysyWrapper_SPR_Wr_socket, a_kysyWrapper_SPR_Wr_die, a_kysyWrapper_SPR_Wr_CCX, a_kysyWrapper_SPR_Wr_Core, 0x0)
		
		v_SPR_PDMAPI = Kysy::PDMAccessAPIs.new(@kysyWrapper_Platform.platformAccess())
		v_SPR_Info = Kysy::PDMAccessInfo.new(Kysy::SPECIAL_REG_WRITE, Kysy::INVALID_PDM_SUB_COMMAND, a_kysyWrapper_SPR_Wr_Addr, 64, a_kysyWrapper_SPR_Wr_Data, Kysy::PDMAccessInfo::WRITE, 4)
		
		v_SPR_PDMAPI.registerMemoryIOAccess(v_SPR_pprCoreTopoIDs, v_SPR_Info)
		
		return v_SPR_Info.readWriteData()
	end
	
	def kysyWrapper_MSR_Rd(a_kysyWrapper_MSR_Rd_Addr, a_kysyWrapper_MSR_Rd_socket, a_kysyWrapper_MSR_Rd_die, a_kysyWrapper_MSR_Rd_CCX, a_kysyWrapper_MSR_Rd_Core, kysyWrapper_MSR_Thread=nil)
		v_MSR_pprCoreTopoIDs = Kysy::PPRCoreTopologyPhysicalIDs.new(a_kysyWrapper_MSR_Rd_socket, a_kysyWrapper_MSR_Rd_die, a_kysyWrapper_MSR_Rd_CCX, a_kysyWrapper_MSR_Rd_Core, 0x0)
		
		v_MSR_PDMAPI = Kysy::PDMAccessAPIs.new(@kysyWrapper_Platform.platformAccess())
		v_MSR_Info = Kysy::PDMAccessInfo.new(Kysy::MSR_REG_READ, Kysy::INVALID_PDM_SUB_COMMAND, a_kysyWrapper_MSR_Rd_Addr, 64, 0x0, Kysy::PDMAccessInfo::READ, 4)
		
		v_MSR_PDMAPI.registerMemoryIOAccess(v_MSR_pprCoreTopoIDs, v_MSR_Info)
		
		return v_MSR_Info.readWriteData()
	end
	
	def kysyWrapper_MSR_Wr(a_kysyWrapper_MSR_Wr_Addr, a_kysyWrapper_MSR_Wr_Data, a_kysyWrapper_MSR_Wr_socket, a_kysyWrapper_MSR_Wr_die, a_kysyWrapper_MSR_Wr_CCX, a_kysyWrapper_MSR_Wr_Core, kysyWrapper_MSR_Thread=nil)
		v_MSR_pprCoreTopoIDs = Kysy::PPRCoreTopologyPhysicalIDs.new(a_kysyWrapper_MSR_Wr_socket, a_kysyWrapper_MSR_Wr_die, a_kysyWrapper_MSR_Wr_CCX, a_kysyWrapper_MSR_Wr_Core, 0x0)
		
		v_MSR_PDMAPI = Kysy::PDMAccessAPIs.new(@kysyWrapper_Platform.platformAccess())
		v_MSR_Info = Kysy::PDMAccessInfo.new(Kysy::MSR_REG_WRITE, Kysy::INVALID_PDM_SUB_COMMAND, a_kysyWrapper_MSR_Wr_Addr, 64, a_kysyWrapper_MSR_Wr_Data, Kysy::PDMAccessInfo::WRITE, 4)
		
		v_MSR_PDMAPI.registerMemoryIOAccess(v_MSR_pprCoreTopoIDs, v_MSR_Info)
		
		return v_MSR_Info.readWriteData()
	end
	
	def kysyWrapper_regAccessByPathBatch (a_regRd_ByPath_Array)
		v_RegisterbatchHandler = @kysyWrapper_Platform.createRegisterBatch
		v_register_obj=[]
		v_return_Data = []
		v_count = 0
		
		for v_reg_obj in  a_regRd_ByPath_Array
			v_register_obj[v_count] = @kysyWrapper_Platform.regByPath("#{v_reg_obj[0]}")
			v_logics = v_register_obj[v_count].accessLogics
			v_acclogic_used = nil

			v_acclogic_check = v_logics.find { |al| al.name =~ /#{v_reg_obj[1].to_s}/}
			v_acclogic_used = v_register_obj[v_count].accessLogic(v_reg_obj[1].to_s)
			
			if (v_acclogic_used != nil)
				if (v_reg_obj[2] == nil)
					v_RegisterbatchHandler.addRead(v_register_obj[v_count], v_acclogic_used)
					puts "using read, String #{v_reg_obj[0]}"
				else
					v_register_obj[v_count].value(v_reg_obj[2]) 
					v_RegisterbatchHandler.addWrite(v_register_obj[v_count], v_acclogic_used)
					puts "using write, data #{v_reg_obj[2].to_s(16)}"
				end
			end
			
			v_count = v_count + 1
			
		end
		v_RegisterbatchHandler.execute
		
		v_count = 0
		for v_count in  0..(v_register_obj.length-1)
			#if (a_regRd_ByPath_Array[v_count][2] == nil)
				v_return_Data[v_count] = v_register_obj[v_count].value
				#puts "read value #{v_register_obj[v_count].value.to_s(16)}."
			#end
		end
		
		return v_return_Data
	end
	
	def kysyWrapper_regWrByPathBatch (a_regRd_ByPath_regPath_AccessTypes_values_Array)
		v_RegisterbatchHandler = @kysyWrapper_Platform.createRegisterBatch
		v_register_obj=[]
		v_count = 0
		
		for v_reg_obj in  a_regRd_ByPath_regPath_AccessTypes_values_Array
			v_register_obj[v_count] = @kysyWrapper_Platform.regByPath("#{v_reg_obj[0]}")
			v_logics = v_register_obj[v_count].accessLogics
			v_acclogic_used = nil
			v_return_Data = []

			v_acclogic_check = v_logics.find { |al| al.name =~ /#{v_reg_obj[1].to_s}/}
			v_acclogic_used = v_register_obj[v_count].accessLogic(v_reg_obj[1].to_s)
			
			if (v_acclogic_used != nil)
				v_register_obj[v_count].value(v_reg_obj[2])
				v_RegisterbatchHandler.addWrite(v_register_obj[v_count], v_acclogic_used)
			end
			
			v_count = v_count + 1
		end
		v_RegisterbatchHandler.execute
	end
	
	def kysyWrapper_MemFill_Dword (a_kysyWrapper_MemFill_Addr, a_kysyWrapper_MemFill_Data_Array, a_kysyWrapper_MemFill_sizeInBytes)
		v_access_size = @non_default_memory_access_sizes[a_kysyWrapper_MemFill_sizeInBytes-1]
		v_bytes = Kysy::Bytes.new(a_kysyWrapper_MemFill_sizeInBytes) # memory size is not hex value, it should be this bytes object
		v_mem = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs,a_kysyWrapper_MemFill_Addr,v_bytes, @memory_Destination_Types, @memory_Access_WRITE_Types)

		v_mem.fill(0)
		(0..( (a_kysyWrapper_MemFill_sizeInBytes/4)-1)).each { |i|
			#puts "i #{i}, value #{a_kysyWrapper_MemFill_Data_Array[i].to_i}."
			v_mem.dword(i,a_kysyWrapper_MemFill_Data_Array[i])
		}
		v_mem.write
	end
	
	### Very slow, waiting for KYSY-2461 ticket for faster usage
	### Load ucode for dGPU
	def kysyWrapper_MemWrLoadUCode (a_kysyWrapper_MemWrLoadUCodeAddr, a_kysyWrapper_ucodeFile)
		v_access_size = Kysy::MEMORY_ACCESS_SIZE_32BIT
		v_bytes = Kysy::Bytes.new(4) # memory size is not hex value, it should be this bytes object
		v_mem = Kysy::PhysicalMemorySpace.mapMemory(@kysyWrapper_Platform.platformAccess(), @pprCoreTopoIDs,a_kysyWrapper_MemWrLoadUCodeAddr,v_bytes, @memory_Destination_Types, @memory_Access_WRITE_Types, v_access_size)
		
		v_file = File.open(a_kysyWrapper_ucodeFile, 'r').each_line do |v_line|
			v_mem.dword(0,v_line.to_i(16))
			v_mem.write
		end
		v_file.close
	end
	
	def kysyWrapper_GetRegObjByPath (a_regRd_ByPath_regPath, a_regRd_ByPath_AccessTypes)
		v_register_obj = @kysyWrapper_Platform.regByPath("#{a_regRd_ByPath_regPath}")
		v_logics = v_register_obj.accessLogics
		#print "access v_logics #{v_logics}\n"
		v_acclogic_used = nil
		
		v_acclogic_check = v_logics.find { |al| al.name =~ /#{a_regRd_ByPath_AccessTypes.to_s}/}
		v_acclogic_used = v_register_obj.accessLogic(a_regRd_ByPath_AccessTypes.to_s)

		if (v_acclogic_used == nil)
			v_register_obj = nil
		end
		
		return v_register_obj
	end

end
