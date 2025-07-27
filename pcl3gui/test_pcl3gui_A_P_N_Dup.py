import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a US Letter plain normal 2-page duplex PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15284
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Printsville_A_P_N_Duplex.pcl=72adddd033ad1636c6124250ecdd9377a88942d30aa6da91293d65dd780241d6
    +name:test_pcl3gui_A_P_N_Dup
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_A_P_N_Dup
        +guid:c4e650e9-732d-4e05-aebd-657bb3806aa2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_A_P_N_Dup(setup_teardown, printjob, outputsaver, tray):
    tray.reset_trays()

    printjob.print_verify('72adddd033ad1636c6124250ecdd9377a88942d30aa6da91293d65dd780241d6')
    outputsaver.save_output()

    logging.info("PCL3GUI US Letter plain normal 2-page duplexcompleted successfully")
