"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_big_file_low_compression_transparent_underflood_45p
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-5338
    +timeout:1800
    +asset:LFP
    +test_framework:TUF
    +delivery_team:LFP
    +feature_team:ProductQA
    +external_files:BigFile_lowCompression_-generic_transparent_underflood_45p.prt=cd3317d0274e6a40632f785518769684cdfe80bac1ee71daa603fb878bdde500
    +test_classification:System
    +name:test_rs_big_file_low_compression_transparent_underflood_45p
    +test:
        +title:test_rs_big_file_low_compression_transparent_underflood_45p
        +guid:234160f2-1896-11ed-821a-73784f55858a
        +dut:
            +type:Simulator, Emulator
            +configuration: DocumentFormat=RasterStreamPlanarICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_big_file_low_compression_transparent_underflood_45p(setup_teardown, printjob, outputsaver, tray, tcl, tclMaia):
    
    try:
        tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")
    except:
        tclMaia.execute("setMediaLoaded ROLL 64 150106")
    
    outputsaver.operation_mode('CRC')

    printjob.print_verify('cd3317d0274e6a40632f785518769684cdfe80bac1ee71daa603fb878bdde500', timeout=2000)
    outputsaver.save_output()

    expected_crc = ["0x9ebbb1c2"]
    
    #Verify that obtained checksums are the expected ones
    outputsaver.verify_output_crc(expected_crc)
