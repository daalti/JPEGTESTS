import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_panoramaimages_hpr927_5m_3
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_panoramaimages_HPR927_5M_3.JPG=e3e510bc084382297091821906875e620bc5bb1aa6f520e8b40ca86c699eb2e2
    +test_classification:System
    +name:test_jpeg_photoimages_panoramaimages_hpr927_5m_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_panoramaimages_hpr927_5m_3
        +guid:d30638c8-00f9-4308-869b-3857f5899320
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_panoramaimages_hpr927_5m_3(setup_teardown, printjob, outputsaver, tray):
    tray.reset_trays()

    printjob.print_verify('e3e510bc084382297091821906875e620bc5bb1aa6f520e8b40ca86c699eb2e2')
    outputsaver.save_output()

    logging.info("Jpeg photoimages_panoramaimages_HPR927_5M_3 file")
