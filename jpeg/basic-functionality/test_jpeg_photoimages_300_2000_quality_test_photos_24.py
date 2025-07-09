import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 24
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_24.jpg=d543b80d11d21075192efdf9b01f9987faa0cb6a57721f10b54bd8c04f1df39a
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_24
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_24
        +guid:e88a5c52-bca6-4637-8478-1b05a3d4626c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_24(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d543b80d11d21075192efdf9b01f9987faa0cb6a57721f10b54bd8c04f1df39a')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 24 - Print job completed successfully")
