
class Sysexam:
    """perform the same sysexam functions on host machine using Wombat interface"""
    def __init__(self, util):
        print ("loading util class..."),
        self.util = util
        print ("done")

    def start_sysexam_on_host(self, sysexam_verify_xml_path, verify_results_csv_path):
        xml_regs_df = self.util.xml_to_dataframe(sysexam_verify_xml_path)
        # print xml_regs_df
        xml_regs_df = self.util.read_register_fields_in_dataframe(xml_regs_df, 'int', True, True) # update bitfield values for each xml_reg
        # print xml_regs_df
        # print xml_regs_df.columns.tolist()
        xml_regs_df = xml_regs_df[['status','path','bitfield','recommend','value']]

        xml_regs_df.to_csv(verify_results_csv_path)
        return 0

    def write_sequence(self, write_sequence_xml_path):
        xml_regs = self.util.read_xml(write_sequence_xml_path)
        xml_regs_df = self.util.xml_to_df(xml_regs)
        xml_regs_df = self.util.write_xml_register_fields(xml_regs_df)
        return 0

    def find_remainder(self, x, y):
        while x>y:
            x = self.util.subtract(x,y)
        print("the remainder is {0}".format(x))


