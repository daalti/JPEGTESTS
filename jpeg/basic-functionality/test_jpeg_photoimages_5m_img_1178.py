import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 5m img 1178
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_5M_IMG_1178.JPG=4c293c1631eab79a47d9f31a40f4b9792141a94487d7d2d58f373e58cf128595
    +test_classification:System
    +name:test_jpeg_photoimages_5m_img_1178
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_5m_img_1178
        +guid:d88f2c22-f0cb-4dfe-adc5-f67f985b6767
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_5m_img_1178(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 170666 and media_length_maximum >= 113777 and  media_width_minimum <= 170666 and media_length_minimum <= 113777:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('4c293c1631eab79a47d9f31a40f4b9792141a94487d7d2d58f373e58cf128595', timeout=300)
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 5M IMG 1178 - Print job completed successfully")
