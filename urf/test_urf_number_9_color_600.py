import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Number-9 Color 600 Page from *Number_9_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Number_9_Color_600.urf=92c06f6d1dc5050e5df7200bf7dca2a58bcc21b48c4e6eeb2bbffcbc23e2cbe8
    +name:test_urf_number_9_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_number_9_color_600_page
        +guid:9b808a18-70df-44a5-92ac-14ee82068f56
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-9_3.875x8.875in &  MediaInputInstalled=Tray3

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_number_9_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('92c06f6d1dc5050e5df7200bf7dca2a58bcc21b48c4e6eeb2bbffcbc23e2cbe8')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Number_9 Color 600 Page - Print job completed successfully")
