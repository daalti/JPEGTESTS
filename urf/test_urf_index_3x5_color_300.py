import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index 3x5 Color 300 from *Index_3x5_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_3x5_Color_300.urf=bbeba90b54f305c990d7d2851bc628a413e394c4a61aa5124f8a0b9bc582dae5
    +name:test_urf_index_3x5_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_3x5_color_300_page
        +guid:64426f4b-f9b8-4622-8777-91b91caa61a9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-3x5_3x5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_3x5_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-3x5_3x5in', default):
        tray.configure_tray(default, 'na_index-3x5_3x5in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('bbeba90b54f305c990d7d2851bc628a413e394c4a61aa5124f8a0b9bc582dae5')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index 3x5 Color 300 page - Print job completed successfully")
