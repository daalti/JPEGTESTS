import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print WxHBitmap-3 page from *PwgCloudPrint-WxHBitmap-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-WxHBitmap-3.pwg=a3578b546236e92198317781b29f07fb358cd8c25f68476b9739b6b2de8f1ef9
    +name:test_pwg_cloud_print_wxh_bitmap_3_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_wxh_bitmap_3_page
        +guid:96833570-f11b-4f6b-8698-f375ae2c6acd
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_wxh_bitmap_3_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a3578b546236e92198317781b29f07fb358cd8c25f68476b9739b6b2de8f1ef9')
    outputsaver.save_output()

    logging.info("PWG Cloud Print WxH Bitmap-3completed successfully")
