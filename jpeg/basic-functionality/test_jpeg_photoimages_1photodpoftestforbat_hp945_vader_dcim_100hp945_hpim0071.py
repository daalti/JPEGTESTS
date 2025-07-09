import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 1photodpoftestforbatm hp945 vader dcim 100hp945 hpim0071
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0071.JPG=34d2105b65aaea33b7ab03e50e51f9a756f6d160514c26903c4595054d0efa62
    +test_classification:System
    +name:test_jpeg_photoimages_1photodpoftestforbat_hp945_vader_dcim_100hp945_hpim0071
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_1photodpoftestforbat_hp945_vader_dcim_100hp945_hpim0071
        +guid:f2821f80-7e51-41c8-b759-bfb25116401c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_1photodpoftestforbat_hp945_vader_dcim_100hp945_hpim0071(setup_teardown, printjob, outputsaver):
    printjob.print_verify('34d2105b65aaea33b7ab03e50e51f9a756f6d160514c26903c4595054d0efa62')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages 1PhotoDPOFTestforBAT hp945 Vader DCIM 100HP945 HPIM0071 - Print job completed successfully")
