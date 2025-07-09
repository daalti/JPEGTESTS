import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 21
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_21.jpg=3a1ec20759147990cf9862dd43a464d15a3628abdd57e3b6d585996c8c38e56b
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_21
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_21
        +guid:82ac5338-0f23-498b-9ce9-20c52448c041
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_21(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3a1ec20759147990cf9862dd43a464d15a3628abdd57e3b6d585996c8c38e56b')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 21 - Print job completed successfully")
