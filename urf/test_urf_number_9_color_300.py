import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Number-9 Color 300 Page from *Number_9_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Number_9_Color_300.urf=172c7648223464af65a2f763b13603a4c2f22ecd066552e80fe23aef66cc6d29
    +name:test_urf_number_9_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_number_9_color_300_page
        +guid:1004ba73-28ab-4d8a-a697-0ac6bd96eb2d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-9_3.875x8.875in &  MediaInputInstalled=Tray3

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_number_9_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('172c7648223464af65a2f763b13603a4c2f22ecd066552e80fe23aef66cc6d29')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Number_9 Color 300 Page - Print job completed successfully")
