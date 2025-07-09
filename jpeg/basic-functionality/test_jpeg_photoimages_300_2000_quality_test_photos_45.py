import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 45
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_45.jpg=65c6e47b8a16cc8134fe3cdf42a2f43a8fc187a5816afec15982746e3e257210
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_45
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_45
        +guid:8b348876-317d-40ce-9175-9a7937ed7bef
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_45(setup_teardown, printjob, outputsaver):
    printjob.print_verify('65c6e47b8a16cc8134fe3cdf42a2f43a8fc187a5816afec15982746e3e257210')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 45 - Print job completed successfully")
