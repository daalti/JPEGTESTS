import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 8k_260x368 Color 600 page from *8k_260x368_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8k_260x368_Color_600.urf=5789ea7b55d3ba888e3507cbccaac142827890b0d305954f0bb6e878e365f2d3
    +name:test_urf_8k_260x368_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8k_260x368_color_600_page
        +guid:77a54b91-f752-4d62-b860-4f3d3fe509a3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8k_260x368_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_8k_260x368mm', default):
        tray.configure_tray(default, 'om_8k_260x368mm', 'stationery')

    printjob.print_verify('5789ea7b55d3ba888e3507cbccaac142827890b0d305954f0bb6e878e365f2d3')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 8k_260x368 Color 600 page - Print job completed successfully")
