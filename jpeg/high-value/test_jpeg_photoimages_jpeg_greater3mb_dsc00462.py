import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_jpeg_greater3mb_dsc00462
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_JPEG_greater3mb_DSC00462.JPG=597a9aa011c812153f2f1da3f72af8ca474959197ebabdece0f1db7baf180d17
    +test_classification:System
    +name:test_jpeg_photoimages_jpeg_greater3mb_dsc00462
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_jpeg_greater3mb_dsc00462
        +guid:d7e0596e-c5df-4860-a854-6f6cfe72a39b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_jpeg_greater3mb_dsc00462(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 453333 and media_length_maximum >= 340000 and  media_width_minimum <= 453333  and media_length_minimum <= 340000:
        tray.configure_tray(default, 'custom', 'stationery')


    printjob.print_verify('597a9aa011c812153f2f1da3f72af8ca474959197ebabdece0f1db7baf180d17')
    outputsaver.save_output()

    logging.info("Jpeg photoimages_JPEG_greater3mb_DSC00462 file")
