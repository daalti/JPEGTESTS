import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages autoalign portrait 3x4 img 0322
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_AutoAlign_Portrait_3x4_IMG_0322.JPG=a68759e088816aa1e0e8764b335a68d0a3fad4dea4db09e7c6456826b6fd09b9
    +test_classification:System
    +name:test_jpeg_photoimages_autoalign_portrait_3x4_img_0322
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_autoalign_portrait_3x4_img_0322
        +guid:2f259c88-87e1-4d22-b226-124519c2149c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_autoalign_portrait_3x4_img_0322(setup_teardown, printjob, outputsaver, tray):
    tray.reset_trays()

    printjob.print_verify('a68759e088816aa1e0e8764b335a68d0a3fad4dea4db09e7c6456826b6fd09b9')
    outputsaver.save_output()

    logging.info("Jpeg photoimages AutoAlign Portrait 3x4 IMG 0322 file")
