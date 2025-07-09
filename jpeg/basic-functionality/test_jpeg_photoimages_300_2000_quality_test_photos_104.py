import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 104
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_104.jpg=f98149047349fc2c16b7702ddf9f624a6094f335ad113a699e3dd88bc85c41f8
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_104
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_104
        +guid:6510a8ff-be0f-4125-ab22-2aee6654dcc3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_104(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f98149047349fc2c16b7702ddf9f624a6094f335ad113a699e3dd88bc85c41f8')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 104 - Print job completed successfully")
