import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 8_5x13 color 600 page from *8_5x13_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8_5x13_Color_600.urf=8d1b6933fe1f14a687571c4995c49236b5054fb5c6fbe8742d475583763955de
    +name:test_urf_8_5x13_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8_5x13_color_600_page
        +guid:f25031eb-7123-48f8-a982-dec0497d5f30
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8_5x13_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('na_foolscap_8.5x13in', default):
        tray.configure_tray(default, 'na_foolscap_8.5x13in', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 85000 and media_length_maximum >= 130000 and  media_width_minimum <= 85000 and media_length_minimum <= 130000:
        tray.configure_tray(default, 'custom', 'stationery')
    

    printjob.print_verify('8d1b6933fe1f14a687571c4995c49236b5054fb5c6fbe8742d475583763955de')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 8_5x13 Color 600 page - Print job completed successfully")
