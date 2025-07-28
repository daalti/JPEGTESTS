import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 5x7 color 300 page from *5x7_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5x7_Color_300.urf=d3c130c98a8ad2d6eabf4e3242890792c9ca1e25710e6a07bea7b531a4050423
    +name:test_urf_5x7_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_5x7_color_300_page
        +guid:fc95adf2-a39a-448b-ab12-c14f49c7f5d9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_5x7_5x7in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_5x7_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index_5x7_5x7in', default):
        tray.configure_tray(default, 'na_index_5x7_5x7in', 'stationery')
    elif tray.is_size_supported('na_5x7_5x7in', default):
        tray.configure_tray(default, 'na_5x7_5x7in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('d3c130c98a8ad2d6eabf4e3242890792c9ca1e25710e6a07bea7b531a4050423')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 5x7 color 300 page - Print job completed successfully")
