import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a A4 draft 3-page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15284
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:MinumC_A4_P_FD_3pgs.pcl=96d3cab1cd5359404517a12076f2ad8613e4ecea8b071062905785af40e8edce
    +name:test_pcl3gui_A4_draft_3pgs
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_A4_draft_3pgs
        +guid:6cbed01c-955f-4329-a0a9-12e0fbb93c42
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_A4_draft_3pgs(setup_teardown, printjob, outputsaver, tray):
    tray.reset_trays()

    printjob.print_verify('96d3cab1cd5359404517a12076f2ad8613e4ecea8b071062905785af40e8edce')
    outputsaver.save_output()

    logging.info("PCL3GUI A4 draft 3-pagecompleted successfully")
