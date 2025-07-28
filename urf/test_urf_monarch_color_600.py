import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Monarch Color 600 Page from *Monarch_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Monarch_Color_600.urf=2ad043c73df52f78ad9b1f2391843b20365a93932b831b4a03dbf9bc427436d5
    +name:test_urf_monarch_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_monarch_color_600_page
        +guid:9c3c5f2e-1d57-4283-8783-6469cf54fdd5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_monarch_3.875x7.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_monarch_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_monarch_3.875x7.5in', default):
        tray.configure_tray(default, 'na_monarch_3.875x7.5in', 'stationery')

    printjob.print_verify('2ad043c73df52f78ad9b1f2391843b20365a93932b831b4a03dbf9bc427436d5')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Monarch Color 600 Page - Print job completed successfully")
