import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index 4x6 Color 600 from *Index_4x6_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_4x6_Color_600.urf=c854b57aa379fe8f9cfaddda4515b9c38075507d0ea795620b824db667b7e60d
    +name:test_urf_index_4x6_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_4x6_color_600_page
        +guid:775e45bf-261a-4d13-a68e-9d65a6292466
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_4x6_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')

    printjob.print_verify('c854b57aa379fe8f9cfaddda4515b9c38075507d0ea795620b824db667b7e60d')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index 4x6 Color 600 Page - Print job completed successfully")
