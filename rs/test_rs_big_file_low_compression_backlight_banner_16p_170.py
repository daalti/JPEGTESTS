"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_big_file_low_compression_backlight_banner_16p_170
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-5338
    +timeout:550
    +asset:LFP
    +test_framework:TUF
    +delivery_team:LFP
    +feature_team:ProductQA
    +external_files:BigFile_lowCompression_-_generic_backlight_banner_16p_170.prt=e27854b4d4819ec20694c85a6396bc4e15aafd121587e46e6ee4495860727ae9
    +test_classification:System
    +name:test_rs_big_file_low_compression_backlight_banner_16p_170
    +test:
        +title:test_rs_big_file_low_compression_backlight_banner_16p_170
        +guid:1858d8fa-1896-11ed-873e-d75b7d621442
        +dut:
            +type:Simulator, Emulator
            +configuration: DocumentFormat=RasterStreamPlanarICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_big_file_low_compression_backlight_banner_16p_170(setup_teardown, printjob, tray, tcl, outputsaver, tclMaia):
    
    try:
        tray.load_simulator_media(tcl, "PVC_BANNER_BACKLIT", "101100")
    except:
        tclMaia.execute("setMediaLoaded ROLL 64 101100")
    
    outputsaver.operation_mode('CRC')

    printjob.print_verify('e27854b4d4819ec20694c85a6396bc4e15aafd121587e46e6ee4495860727ae9', timeout=500)
    outputsaver.save_output()

    expected_crc = ["0xd2752d17"]
    
    #Verify that obtained checksums are the expected ones
    outputsaver.verify_output_crc(expected_crc)
