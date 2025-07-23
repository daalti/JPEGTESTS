import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print WxHBitmap-1 page from *PwgCloudPrint-WxHBitmap-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-WxHBitmap-1.pwg=f9d53207963887fac374d5f173a385f701e39bf5a03906374d7ec78750389962
    +name:test_pwg_cloud_print_wxh_bitmap_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_wxh_bitmap_1_page
        +guid:8195fb74-1059-45bb-9c21-5a6e086e43a6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_wxh_bitmap_1_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('f9d53207963887fac374d5f173a385f701e39bf5a03906374d7ec78750389962')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PWG Cloud Print WxH Bitmap-1completed successfully")
