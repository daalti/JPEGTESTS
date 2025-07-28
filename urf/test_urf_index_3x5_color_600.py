import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index 3x5 Color 600 from *Index_3x5_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_3x5_Color_600.urf=cc60910c26e7c97b571635cc5d63eab4ed44295c06c052c87b27ee183b39f003
    +name:test_urf_index_3x5_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_3x5_color_600_page
        +guid:564591ab-c735-41fc-904b-e8ca1720d94d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-3x5_3x5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_3x5_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-3x5_3x5in', default):
        tray.configure_tray(default, 'na_index-3x5_3x5in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('cc60910c26e7c97b571635cc5d63eab4ed44295c06c052c87b27ee183b39f003')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index 3x5 Color 600 page - Print job completed successfully")
