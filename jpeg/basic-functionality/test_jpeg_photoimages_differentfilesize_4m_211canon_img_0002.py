import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages differentfilesize 4m 211canon img 0002
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_differentfilesize_4M_211CANON_IMG_0002.JPG=ff074792fba217f14d2fad33955f22c5f86095d72f43e6037837701715fa21ea
    +test_classification:System
    +name:test_jpeg_photoimages_differentfilesize_4m_211canon_img_0002
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_differentfilesize_4m_211canon_img_0002
        +guid:5cbfd2c3-1da1-441d-b1b3-be13efb45a09
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_differentfilesize_4m_211canon_img_0002(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 202666 and media_length_maximum >= 152000 and  media_width_minimum <= 202666 and media_length_minimum <= 152000:
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('ff074792fba217f14d2fad33955f22c5f86095d72f43e6037837701715fa21ea')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages differentfilesize 4M 211CANON IMG 0002 - Print job completed successfully")
