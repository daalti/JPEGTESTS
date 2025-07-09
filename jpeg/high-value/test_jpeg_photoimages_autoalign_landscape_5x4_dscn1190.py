import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages autoalign landscape 5x4 dscn1190
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_AutoAlign_Landscape_5x4_DSCN1190.JPG=f7cc84d7e8c40f5fe3c9c95959a2bc8e69506f260865051c9d979db0ccc5128b
    +test_classification:System
    +name:test_jpeg_photoimages_autoalign_landscape_5x4_dscn1190
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_autoalign_landscape_5x4_dscn1190
        +guid:22ef2658-5a3d-4d42-a6c3-67d73f15da15
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_autoalign_landscape_5x4_dscn1190(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 68266 and media_length_maximum >= 51200 and  media_width_minimum <= 68266  and media_length_minimum <= 51200:
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('f7cc84d7e8c40f5fe3c9c95959a2bc8e69506f260865051c9d979db0ccc5128b')
    outputsaver.save_output()
    tray.reset_trays()
    logging.info("Jpeg photoimages AutoAlign Landscape 5x4 DSCN1190 file")
