import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages defectiveimages cr222024 photo
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_Defectiveimages_CR222024_photo.JPG=8d048d9866c8db52ab7fb0eb1cdb8e024c8ad2f43c922453af85ddcab3e4a80c
    +test_classification:System
    +name:test_jpeg_photoimages_defectiveimages_cr222024_photo
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_defectiveimages_cr222024_photo
        +guid:f52240be-fbe6-4656-ab07-afddb26f43de
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_defectiveimages_cr222024_photo(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 453333 and media_length_maximum >= 340000 and  media_width_minimum <= 453333 and media_length_minimum <= 340000:
        tray.configure_tray(default, 'custom', 'stationery')


    printjob.print_verify('8d048d9866c8db52ab7fb0eb1cdb8e024c8ad2f43c922453af85ddcab3e4a80c')
    outputsaver.save_output()

    logging.info("Jpeg photoimages Defectiveimages CR222024 photo file")
