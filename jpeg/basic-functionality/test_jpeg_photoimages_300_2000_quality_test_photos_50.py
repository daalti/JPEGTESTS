import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 50
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_50.jpg=143829ed3af12fe47429e199b4d725b6bb4e1ce44138debc6e5c2e06899d0393
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_50
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_50
        +guid:5109cacd-9cf7-4338-a139-ab7e752e2026
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_50(setup_teardown, printjob, outputsaver):
    printjob.print_verify('143829ed3af12fe47429e199b4d725b6bb4e1ce44138debc6e5c2e06899d0393')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 50 - Print job completed successfully")
