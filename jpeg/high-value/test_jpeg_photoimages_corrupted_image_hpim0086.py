import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages corrupted image hpim0086
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_Corrupted_image_HPIM0086.JPG=344788233baa04baf642da4985648ad970fbb293285be13529ac743264435ad6
    +test_classification:System
    +name:test_jpeg_photoimages_corrupted_image_hpim0086
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_corrupted_image_hpim0086
        +guid:33daba10-4519-433e-ae60-d0babd859660
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_corrupted_image_hpim0086(setup_teardown, printjob, outputsaver):
    printjob.print_verify('344788233baa04baf642da4985648ad970fbb293285be13529ac743264435ad6','FAILED')
    outputsaver.save_output()

    logging.info("Jpeg photoimages Corrupted image HPIM0086 file")
