import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages resolution jpg jpg5
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_resolution_jpg_jpg5.jpg=39485a0ae7f97d3ab8d4c4753bee2d53ac87d9ac2e77ea355c4cd88374cb9c4d
    +test_classification:System
    +name:test_jpeg_photoimages_resolution_jpg_jpg5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_resolution_jpg_jpg5
        +guid:3c4411d0-64b7-4a13-b851-6b2b6cc61977
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_resolution_jpg_jpg5(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('39485a0ae7f97d3ab8d4c4753bee2d53ac87d9ac2e77ea355c4cd88374cb9c4d')
    outputsaver.save_output()

    logging.info("Jpeg photoimages resolution jpg jpg5 file")
