import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job which exercises driverware for Sub Media Types HP brochure-matte using a US letter normal 1-page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-6338
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Wedding_Vision_A_HPBroch_Matte_N.pcl=9fb185eeb0b0ce592a873f0a2f17ccb7c231a5add0dd930ad0468a7243312031
    +name:test_pcl3gui_sub_media_type_brochure_matte
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_sub_media_type_brochure_matte
        +guid:6cfce42a-7417-44a6-bed5-d0007123f103
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_sub_media_type_brochure_matte(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default) and tray.is_type_supported('com.hp-matte-brochure', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'com.hp-matte-brochure')

    printjob.print_verify('9fb185eeb0b0ce592a873f0a2f17ccb7c231a5add0dd930ad0468a7243312031')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PCL3GUI Sub Media Type HP brochure-matte US letter normal 1-pagecompleted successfully")
