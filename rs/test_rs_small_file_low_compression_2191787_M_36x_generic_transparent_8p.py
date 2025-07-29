"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_small_file_low_compression_2191787_M_36x_generic_transparent_8p
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-5338
    +timeout:450
    +asset:LFP
    +test_framework:TUF
    +delivery_team:LFP
    +feature_team:ProductQA
    +external_files:SmallFile_lowCompression_-_2191787_M_36x_generic_transparent_8p.prt=5be56ba203112920f37f81265204a2006129e05fb69efa8ab2b18ae609dc95ad
    +test_classification:System
    +name:test_rs_small_file_low_compression_2191787_M_36x_generic_transparent_8p
    +test:
        +title:test_rs_small_file_low_compression_2191787_M_36x_generic_transparent_8p
        +guid:502c8fb0-1896-11ed-bf62-b3e0f2a26e6f
        +dut:
            +type:Simulator, Emulator
            +configuration: DocumentFormat=RasterStreamPlanarICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_small_file_low_compression_2191787_M_36x_generic_transparent_8p(setup_teardown, printjob, outputsaver, tray, tcl, tclMaia):
    
    try:
        tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")
    except:
        tclMaia.execute("setMediaLoaded ROLL 64 150106")
    
    outputsaver.operation_mode('CRC')

    printjob.print_verify('5be56ba203112920f37f81265204a2006129e05fb69efa8ab2b18ae609dc95ad', timeout=500)
    outputsaver.save_output()

    expected_crc = ["0x305a2861"]
    
    #Verify that obtained checksums are the expected ones
    outputsaver.verify_output_crc(expected_crc)
