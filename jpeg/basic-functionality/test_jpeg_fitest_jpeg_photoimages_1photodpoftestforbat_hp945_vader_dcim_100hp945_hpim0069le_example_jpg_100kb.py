import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 1photodpoftestforbat hp945 vader dcim 100hp945 hpim0069
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0069.JPG=3fd5bf0f2e753f3c417e81304a978e7264095c000a6c5f63e90500dbd2797129
    +test_classification:System
    +name:test_jpeg_fitest_jpeg_photoimages_1photodpoftestforbat_hp945_vader_dcim_100hp945_hpim0069le_example_jpg_100kb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_fitest_jpeg_photoimages_1photodpoftestforbat_hp945_vader_dcim_100hp945_hpim0069le_example_jpg_100kb
        +guid:1d6629af-c70c-46be-a64a-e67a18f7f8f5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_fitest_jpeg_photoimages_1photodpoftestforbat_hp945_vader_dcim_100hp945_hpim0069le_example_jpg_100kb(setup_teardown, printjob, outputsaver, tray):

    default = tray.get_default_source()
    
    default_size = tray.get_default_size(default)

    if tray.is_size_supported(default_size, default):
        tray.configure_tray(default, default_size, 'stationery')

    printjob.print_verify('3fd5bf0f2e753f3c417e81304a978e7264095c000a6c5f63e90500dbd2797129')
    outputsaver.save_output()
    tray.reset_trays()
    logging.info("Jpeg file example photoimages 1PhotoDPOFTestforBAT hp945 Vader DCIM 100HP945 HPIM0069 - Print job completed successfully")
