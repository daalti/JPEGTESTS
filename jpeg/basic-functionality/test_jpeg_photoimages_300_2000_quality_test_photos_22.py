import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 22
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_22.jpg=8a479ef7128345004b50b10056901496642e199ec29d434c5fa7cb6cffc42b57
    +test_classification:System
    +name:test_jpeg_photoimages_300_2000_quality_test_photos_22
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_22
        +guid:9e29a079-a9bd-400e-b778-0aed8c417515
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_300_2000_quality_test_photos_22(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8a479ef7128345004b50b10056901496642e199ec29d434c5fa7cb6cffc42b57')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 22 - Print job completed successfully")
