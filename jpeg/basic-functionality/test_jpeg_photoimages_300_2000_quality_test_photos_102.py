import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 102
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_102.jpg=fdb091a4bccb830fdb1421688f74e708827434b6d7e1c6cde9db12b39c1b957b
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_102
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_102
        +guid:7842498f-112d-43ad-afed-3b4edc638cb0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_102(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fdb091a4bccb830fdb1421688f74e708827434b6d7e1c6cde9db12b39c1b957b')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 102 - Print job completed successfully")
