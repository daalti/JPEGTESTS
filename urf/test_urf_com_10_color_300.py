import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf Com-10 Color 300 from *Com-10_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Com-10_Color_300.urf=6864568ba0cd1a401a56ef797e931574e86566ce255a7650e75fc780e3b2f126
    +name:test_urf_com_10_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_com_10_color_300_page
        +guid:4d219e13-369a-4cca-9a18-7eba6625bee0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-10_4.125x9.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_com_10_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default):
        tray.configure_tray(default, 'na_number-10_4.125x9.5in', 'stationery')

    printjob.print_verify('6864568ba0cd1a401a56ef797e931574e86566ce255a7650e75fc780e3b2f126')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Com-10 Color 300 page - Print job completed successfully")
