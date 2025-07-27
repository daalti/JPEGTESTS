import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job which exercises driverware for com.hp-trifold-brochure-glossy-180gsm Media Types  using a US letter normal 1-page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-6338
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:HP_Tri-fold_Brochure_Paper_Glossy.pcl=b982c46ef54f82835347f7908c57c162a3ca7e13cb10b01e73a92a2217748c7a
    +name:test_pcl3gui_media_type_Trifold_Glossy180
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_media_type_Trifold_Glossy180
        +guid:5cd3fd3f-df03-4ffb-89c2-dfe50d208e9d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_media_type_Trifold_Glossy180(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default) and tray.is_type_supported('com.hp-trifold-brochure-glossy-180gsm', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'com.hp-trifold-brochure-glossy-180gsm')

    printjob.print_verify('b982c46ef54f82835347f7908c57c162a3ca7e13cb10b01e73a92a2217748c7a')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PCL3GUI Media Type trifold-brochure-glossy-180gsm US letter normal 1-pagecompleted successfully")