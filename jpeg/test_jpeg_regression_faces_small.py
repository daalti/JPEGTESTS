import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Regression of faces small Page from *faces_small.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:faces_small.jpg=19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc
    +test_classification:System
    +name:test_jpeg_regression_faces_small
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_faces_small
        +guid:86ce0eca-17e3-43d4-8aa9-bbaf47fc6c4e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_regression_faces_small(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("JPEG Regression faces small Page - Print job completed successfully")
