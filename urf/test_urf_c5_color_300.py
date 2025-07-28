import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178022 Simple print job of urf C5 Color 300 from *C5_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:C5_Color_300.urf=da6a116dd501b5b3e9a52a4bbb3743e6db25392773d236a086ded43f4041a4ea
    +name:test_urf_c5_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_c5_color_300_page
        +guid:89b68d24-e971-46bf-a576-3ecf35402553
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_c5_162x229mm
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_c5_color_300_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('iso_c5_162x229mm', default):
        tray.configure_tray(default, 'iso_c5_162x229mm', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 63766 and media_length_maximum >= 90133 and  media_width_minimum <= 63766 and media_length_minimum <= 90133:
        tray.configure_tray(default, 'custom', 'stationery')    
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('da6a116dd501b5b3e9a52a4bbb3743e6db25392773d236a086ded43f4041a4ea')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    logging.info("URF C5 Color 300 page - Print job completed successfully")
