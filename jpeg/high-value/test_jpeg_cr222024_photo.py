import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of cr222024_photo
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:CR222024_photo.JPG=4491f594e123d85879be3d23a3b8d8c94eee91510d5cdc3e25bf882309110211
    +test_classification:System
    +name:test_jpeg_cr222024_photo
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_cr222024_photo
        +guid:af485faf-1e63-4807-b80c-370301418f66
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_cr222024_photo(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 80000 and media_length_maximum >= 110000 and media_width_minimum <= 80000 and media_length_minimum <= 110000:
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('4491f594e123d85879be3d23a3b8d8c94eee91510d5cdc3e25bf882309110211')
    outputsaver.save_output()
    tray.reset_trays()
    logging.info("Jpeg CR222024_photo")
