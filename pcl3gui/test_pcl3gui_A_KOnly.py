import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job which exercises driverware for KOnly using a US letter plain normal 1-page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-6338
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Quantum_polygon_banding_Asize_kOnly_PN.pcl=10252cdf8ccc8ccacaf9c787ac1caca9e53782f3c872bfa22059dd5ea14a49da
    +name:test_pcl3gui_KOnly_A_P_N
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_KOnly_A_P_N
        +guid:85ce9a8f-018a-48bd-8251-668c85332f8f
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
def test_pcl3gui_KOnly_A_P_N(setup_teardown, printjob, outputsaver):
    printjob.print_verify('10252cdf8ccc8ccacaf9c787ac1caca9e53782f3c872bfa22059dd5ea14a49da')
    outputsaver.save_output()

    logging.info("PCL3GUI KOnly US letter plain normal 1-pagecompleted successfully")
