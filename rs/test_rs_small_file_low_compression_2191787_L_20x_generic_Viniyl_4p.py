"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-5338
    +timeout:300
    +asset:LFP
    +test_framework:TUF
    +delivery_team:LFP
    +feature_team:ProductQA
    +external_files:SmallFile_lowCompression_-_2191787_L_20x_Generic_Viniyl_4p.prt=6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06
    +test_classification:System
    +name:test_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p
    +test:
        +title:test_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p
        +guid:307abcdc-1896-11ed-ad34-fb87f3b4cd50
        +dut:
            +type:Simulator, Emulator
            +configuration: DocumentFormat=RasterStreamPlanarICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p(setup_teardown, printjob, outputsaver):
    
    outputsaver.operation_mode('CRC')

    printjob.print_verify('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06', timeout=300)
    outputsaver.save_output()

    expected_crc = ["0x20ff185f"]
    
    #Verify that obtained checksums are the expected ones
    outputsaver.verify_output_crc(expected_crc)
