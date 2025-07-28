import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178028 Simple print job of Urf Number-10 Color 600 Page from *Number-10_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Number-10_Color_600.urf=8d595b53cdf90287cb1991f9a7ebfae5f99cc51f929514658f1cda625a1236e0
    +name:test_urf_number_10_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_number_10_color_600_page
        +guid:71a7e6a1-752a-45b9-aaba-5d7f42ae2cd6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-10_4.125x9.5in
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_number_10_color_600_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default):
        tray.configure_tray(default, 'na_number-10_4.125x9.5in', 'stationery')
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('8d595b53cdf90287cb1991f9a7ebfae5f99cc51f929514658f1cda625a1236e0')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF Number-10 Color 600 Page - Print job completed successfully")
