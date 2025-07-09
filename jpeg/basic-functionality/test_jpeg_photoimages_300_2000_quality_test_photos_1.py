import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_1.jpg=8f2683c349abb62cf15b5eb799d9c35d05ed45db7f3ba6863629421275921d65
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_1
        +guid:0b25c9a9-72e7-4b18-a783-d34f97182504
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8f2683c349abb62cf15b5eb799d9c35d05ed45db7f3ba6863629421275921d65')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 1 - Print job completed successfully")
