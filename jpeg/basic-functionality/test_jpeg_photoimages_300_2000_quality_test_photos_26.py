import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 26
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_26.jpg=81fc17818224be0036736ce53e5804c5695fe1a4606c96fe694f4b0034c510da
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_26
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_26
        +guid:4a9db118-5ff7-4061-9465-b9bcf069678f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_26(setup_teardown, printjob, outputsaver):
    printjob.print_verify('81fc17818224be0036736ce53e5804c5695fe1a4606c96fe694f4b0034c510da')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 26 - Print job completed successfully")
