import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 101
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_101.jpg=27e760e042664eccb2b50c1fad3417297544641071d6d012b86c2f32a8d89bf1
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_101
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_101
        +guid:c0b60571-c627-407e-9087-811887c50967
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_101(setup_teardown, printjob, outputsaver):
    printjob.print_verify('27e760e042664eccb2b50c1fad3417297544641071d6d012b86c2f32a8d89bf1')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 101 - Print job completed successfully")
