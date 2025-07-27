import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a US Letter plain normal one page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15284
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:OldTimeRadio_A_Plain_Normal.pcl=9b408bfc6b5b13d21a6e1a01f81a2f1c1011a64895a64e89c1733ab060b15077
    +name:test_pcl3gui_A_P_N
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_A_P_N
        +guid:0b27c34f-a972-4aee-920b-6425d21377c2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_A_P_N(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9b408bfc6b5b13d21a6e1a01f81a2f1c1011a64895a64e89c1733ab060b15077')
    outputsaver.save_output()

    logging.info("PCL3GUI US Letter plain normal one pagecompleted successfully")
