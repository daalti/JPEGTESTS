import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_exif2.3_exif2.3_dsci0018
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_Exif2.3_Exif2.3_DSCI0018.JPG=72f5dce85ec7f14f1e021c90fb981da4ee517bd9cc3d32f9855d409a75747b07
    +test_classification:System
    +name:test_jpeg_photoimages_exif2_3_exif2_3_dsci0018
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_exif2_3_exif2_3_dsci0018
        +guid:9007aa0b-cfad-4317-a188-20f11d1cfa94
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_exif2_3_exif2_3_dsci0018(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
   
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 480000 and media_length_maximum >= 360000 and  media_width_minimum <= 480000 and media_length_minimum <= 360000:
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('72f5dce85ec7f14f1e021c90fb981da4ee517bd9cc3d32f9855d409a75747b07')
    outputsaver.save_output()

    logging.info("Jpeg photoimages_Exif2.3_Exif2.3_DSCI0018 file")
