import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_lessthan3megapixelphoto_dscn4744
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_lessthan3MegaPixelphoto_DSCN4744.JPG=6666d5ccbf4fb13317b183faa35e96f7050b1e29f6161cfd28050accebf64e17
    +test_classification:System
    +name:test_jpeg_photoimages_lessthan3megapixelphoto_dscn4744
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_lessthan3megapixelphoto_dscn4744
        +guid:eb75a5bc-b291-471b-8685-9d98a9411eda
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_lessthan3megapixelphoto_dscn4744(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 40000 and media_length_maximum >= 53333 and  media_width_minimum <= 40000  and media_length_minimum <= 53333:
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('6666d5ccbf4fb13317b183faa35e96f7050b1e29f6161cfd28050accebf64e17')
    outputsaver.save_output()
    tray.reset_trays()
    logging.info("Jpeg photoimages_lessthan3MegaPixelphoto_DSCN4744 file")
