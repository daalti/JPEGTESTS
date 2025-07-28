import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178027 Simple print job of Urf Index 5x8 from *na_index_5x8.urf file
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:180
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:na_index_5x8.urf=55bb9ae41931e38bcf18c6fa23e9f0c51d4bb89dc51ce6bab34c1af1c80cb811
    +test_classification:System
    +name:test_urf_index_5x8_page
    +test:
        +title:test_urf_index_5x8_page
        +guid:1c4c969e-1903-49a9-934c-bdadc75e2240
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-5x8_5x8in
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_5x8_page(setup_teardown, reset_tray, printjob, outputsaver, tray, udw):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-5x8_5x8in', default):
        tray.configure_tray(default, 'na_index-5x8_5x8in', 'stationery')

    printjob.print_verify('55bb9ae41931e38bcf18c6fa23e9f0c51d4bb89dc51ce6bab34c1af1c80cb811')
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
