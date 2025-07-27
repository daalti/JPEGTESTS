import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job which exercises driverware for speed-mech using a US letter plain normal 4-page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-6338
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Delenit_A_P_N_4pgs.pcl=c4b5843da0da11f404178e6fcafafa13aae608b777913fdc6af16e5e848a7077
    +name:test_pcl3gui_speedmech_A_4pgs
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_speedmech_A_4pgs
        +guid:18d32947-3800-4e79-b492-e5c0425a618b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_speedmech_A_4pgs(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c4b5843da0da11f404178e6fcafafa13aae608b777913fdc6af16e5e848a7077')
    outputsaver.save_output()

    logging.info("PCL3GUI speed-mech US letter plain normal 4-pagecompleted successfully")
