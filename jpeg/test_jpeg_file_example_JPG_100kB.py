import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg file of 100kB from *file_example_JPG_100kB.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_example_JPG_100kB.jpg=88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6
    +test_classification:System
    +name:test_jpeg_file_example_JPG_100kB
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_file_example_JPG_100kB
        +guid:9b4ed8d0-e252-4596-aa81-ee0fcd483e0b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_file_example_JPG_100kB(setup_teardown, printjob, outputsaver,tray, udw):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum > 85000 and media_length_maximum >= 110000 and media_width_minimum < 85000 and media_length_minimum <= 110000:
        tray.configure_tray(default, 'custom', 'stationery')
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6', timeout=360)
    outputsaver.save_output()
    tray.reset_trays()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("Jpeg file example JPG 100kB Page - Print job completed successfully")
