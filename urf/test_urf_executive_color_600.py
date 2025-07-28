import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Executive Color 600 from *Executive_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Executive_Color_600.urf=0d596a0a1a49bf52626a68b80c78720cd86f9e523e4c846e285032713ad24efb
    +name:test_urf_executive_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_executive_color_600_page
        +guid:c00c5723-7949-40fe-95e2-7b5572f4d32e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_executive_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_executive_7.25x10.5in', default):
        tray.configure_tray(default, 'na_executive_7.25x10.5in', 'stationery')

    printjob.print_verify('0d596a0a1a49bf52626a68b80c78720cd86f9e523e4c846e285032713ad24efb')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Executive Color 600 page - Print job completed successfully")
