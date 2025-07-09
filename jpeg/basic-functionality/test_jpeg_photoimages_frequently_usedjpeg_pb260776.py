import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages frequently-usedjpeg pb260776
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_Frequently-usedJPEG_PB260776.JPG=85db63fbd7f31121d4936a1a12d8fab3c76129b226b6d0f75764c0c7ba552f1d
    +test_classification:System
    +name:test_jpeg_photoimages_frequently_usedjpeg_pb260776
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_frequently_usedjpeg_pb260776
        +guid:b7acef96-0de3-4dfc-8f57-5f30aa7d1c3c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_frequently_usedjpeg_pb260776(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 146751 and media_length_maximum >= 110063 and  media_width_minimum <=  146751 and media_length_minimum <= 110063:
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('85db63fbd7f31121d4936a1a12d8fab3c76129b226b6d0f75764c0c7ba552f1d')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages Frequently-usedJPEG PB260776 - Print job completed successfully")
