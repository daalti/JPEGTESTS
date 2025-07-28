import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178026 Simple print job of Urf Legal Color 300 from *Legal_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Legal_Color_300.urf=2042313a631de659d06dc5ae09b531c4637dde2bb444ea21314d01c21b4e10ce
    +name:test_urf_legal_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_legal_color_300_page
        +guid:910ac34d-e2a4-4377-abc7-84d4bd9bb39a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_legal_color_300_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 85000 and media_length_maximum >= 140000 and  media_width_minimum <= 85000 and media_length_minimum <= 140000:
        tray.configure_tray(default, 'custom', 'stationery')  
    outputsaver.validate_crc_tiff(udw)  
    printjob.print_verify('2042313a631de659d06dc5ae09b531c4637dde2bb444ea21314d01c21b4e10ce')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF Legal Color 300 Page - Print job completed successfully")
