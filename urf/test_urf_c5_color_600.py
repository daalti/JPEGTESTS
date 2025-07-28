import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf C5 Color 600 from *C5_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:C5_Color_600.urf=c5ec056aa515083a82c5e21da869032b191629ce036bd2a6e38b4faecf369bef
    +name:test_urf_c5_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_c5_color_600_page
        +guid:a645d580-14a5-4ed7-abc5-2e7b6c7bba8c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_c5_162x229mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_c5_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('iso_c5_162x229mm', default):
        tray.configure_tray(default, 'iso_c5_162x229mm', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 63766 and media_length_maximum >= 90133 and  media_width_minimum <= 63766 and media_length_minimum <= 90133:
        tray.configure_tray(default, 'custom', 'stationery')    

    printjob.print_verify('c5ec056aa515083a82c5e21da869032b191629ce036bd2a6e38b4faecf369bef')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF C5 Color 600 page - Print job completed successfully")
