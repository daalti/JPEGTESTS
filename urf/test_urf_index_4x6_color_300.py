import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index 4x6 Color 300 from *Index_4x6_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_4x6_Color_300.urf=be96e88236acd547a69d0c44bf6e838def95c2817ac03c4adde5b7bc1fd3c016
    +name:test_urf_index_4x6_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_4x6_color_300_page
        +guid:124ca763-d6dc-4d6a-9e68-c5c10c29b33c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_4x6_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')

    printjob.print_verify('be96e88236acd547a69d0c44bf6e838def95c2817ac03c4adde5b7bc1fd3c016')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index 4x6 Color 300 Page - Print job completed successfully")
