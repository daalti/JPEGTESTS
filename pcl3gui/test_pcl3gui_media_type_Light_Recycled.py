import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job which exercises driverware for stationery-lightweight Media Types  using a US letter normal 1-page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-6338
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Plain_Paper_Light_Recycled.pcl=4cded04ea1c693f58dab66ab5320ac8d87cddddbee8498065ab28bea53e91394
    +name:test_pcl3gui_media_type_Light_Recycled
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_media_type_Light_Recycled
        +guid:1281c41b-3c42-4e50-840d-20b7f0340a0a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & MediaType=Plain

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_media_type_Light_Recycled(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default) and tray.is_type_supported('stationery-lightweight', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery-lightweight')

    printjob.print_verify('4cded04ea1c693f58dab66ab5320ac8d87cddddbee8498065ab28bea53e91394')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PCL3GUI Media Type HP stationery-lightweight US letter normal 1-pagecompleted successfully")
