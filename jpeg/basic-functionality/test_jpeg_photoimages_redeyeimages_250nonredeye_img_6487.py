import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages redeyeimages 250nonredeye img 6487

    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_Redeyeimages_250Nonredeye_IMG_6487.JPG=1497ed339f914418a8fb1329a1117c3668266884fbef99901ec6dcfaa73631de
    +test_classification:System
    +name:test_jpeg_photoimages_redeyeimages_250nonredeye_img_6487
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_redeyeimages_250nonredeye_img_6487
        +guid:e987a5a6-e2b6-4d05-b676-fccd724129dd
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_redeyeimages_250nonredeye_img_6487(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1497ed339f914418a8fb1329a1117c3668266884fbef99901ec6dcfaa73631de')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages Redeyeimages 250Nonredeye IMG 6487 - Print job completed successfully")
