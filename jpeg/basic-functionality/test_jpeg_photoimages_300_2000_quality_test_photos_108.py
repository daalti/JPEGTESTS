import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 108
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_108.jpg=d4adbb615180a94df9fc92a517ab55609eb0a7b824e93b073b210104916e45dd
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_108
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_108
        +guid:2f9d2a81-fb20-4d35-bc34-6701d5cec7e8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_108(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d4adbb615180a94df9fc92a517ab55609eb0a7b824e93b073b210104916e45dd')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 108 - Print job completed successfully")
