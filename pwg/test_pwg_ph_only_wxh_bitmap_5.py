import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-WxHBitmap-5.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-WxHBitmap-5.pwg=2df745b8bb450ee22b75acbde2662138ff59c346ae9ebe819d46086d12141b58
    +name:test_pwg_ph_only_wxh_bitmap_5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_wxh_bitmap_5
        +guid:9696ead1-3b1b-4738-bdfc-e402c335c779
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_wxh_bitmap_5(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_executive_7.25x10.5in', default):
        tray.configure_tray(default, 'na_executive_7.25x10.5in', 'stationery')

    printjob.print_verify('2df745b8bb450ee22b75acbde2662138ff59c346ae9ebe819d46086d12141b58', 'FAILED')
    outputsaver.save_output()
    tray.reset_trays()
