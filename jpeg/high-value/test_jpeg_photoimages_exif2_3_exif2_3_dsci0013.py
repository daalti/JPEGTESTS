import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_exif2.3_exif2.3_dsci0013
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_Exif2.3_Exif2.3_DSCI0013.JPG=d1792461f8ef786f54d0bca2872e939d679f59bf169dd0a66ebbeb1a53ac289a
    +test_classification:System
    +name:test_jpeg_photoimages_exif2_3_exif2_3_dsci0013
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_exif2_3_exif2_3_dsci0013
        +guid:2937c878-57b9-4f22-8f31-4ac60e31baa5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_exif2_3_exif2_3_dsci0013(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
 
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 480000 and media_length_maximum >= 360000 and  media_width_minimum <= 480000 and media_length_minimum <= 360000:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('d1792461f8ef786f54d0bca2872e939d679f59bf169dd0a66ebbeb1a53ac289a')
    outputsaver.save_output()

    logging.info("Jpeg photoimages_Exif2.3_Exif2.3_DSCI0013 file")
