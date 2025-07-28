import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf B5 Color 300 from *B5_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:B5_Color_300.urf=5846af426a0a28f710ff4bcf1c1ede8a0da018873f21bd1c8cf9bf86fe1be211
    +name:test_urf_b5_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_b5_color_300_page
        +guid:55ea6eea-2a44-404e-aedc-975461fb21d7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_b5_176x250mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_b5_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_b5_176x250mm', default):
        tray.configure_tray(default, 'iso_b5_176x250mm', 'stationery')

    printjob.print_verify('5846af426a0a28f710ff4bcf1c1ede8a0da018873f21bd1c8cf9bf86fe1be211')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF B5 Color 300 page - Print job completed successfully")
