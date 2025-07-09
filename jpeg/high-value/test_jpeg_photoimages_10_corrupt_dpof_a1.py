import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages 10 corrupt dpof a1
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_10_corrupt_DPOF_a1.jpg=150c0425c6a2ab2de1209cd09587ba4b2a8d0a0f7de0e0b7adb5a1947ae6db34
    +test_classification:System
    +name:test_jpeg_photoimages_10_corrupt_dpof_a1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_10_corrupt_dpof_a1
        +guid:8e30f716-5320-40d3-adf0-88c8242ec49e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_10_corrupt_dpof_a1(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')

    elif tray.is_size_supported('custom', default) and media_width_maximum >= 48611 and media_length_maximum >= 55555 and  media_width_minimum <= 48611  and media_length_minimum <= 55555:
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('150c0425c6a2ab2de1209cd09587ba4b2a8d0a0f7de0e0b7adb5a1947ae6db34')
    outputsaver.save_output()
    tray.reset_trays()
    logging.info("Jpeg photoimages 10 corrupt DPOF a1 file")
