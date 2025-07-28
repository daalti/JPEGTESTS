import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index 5x8 Color 300 from *Index_5x8_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_5x8_Color_300.urf=3a79d96259508d520d24dd0e043a2649ce85f002e00b7821c6ede491b333ea39
    +name:test_urf_index_5x8_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_5x8_color_300_page
        +guid:989f3bb2-6445-4185-8db3-ec0dc895005e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-5x8_5x8in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_5x8_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-5x8_5x8in', default):
        tray.configure_tray(default, 'na_index-5x8_5x8in', 'stationery')

    printjob.print_verify('3a79d96259508d520d24dd0e043a2649ce85f002e00b7821c6ede491b333ea39')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index 5x8 Color 300 Page - Print job completed successfully")
