import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 17Page_ctulineu.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:17Page-ctulineu.obj=4a755467daaed2c48a4dca3dc13e5266319258242cf5497d7eb39423fbffae66
    +test_classification:System
    +name: test_pcl5_highvalue_17page_ctulineu
    +test:
        +title: test_pcl5_highvalue_17page_ctulineu
        +guid:6ac4b94b-7232-49bd-b28a-05b1e9ddaad0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_17page_ctulineu(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('4a755467daaed2c48a4dca3dc13e5266319258242cf5497d7eb39423fbffae66',timeout=600)
    outputsaver.save_output()
