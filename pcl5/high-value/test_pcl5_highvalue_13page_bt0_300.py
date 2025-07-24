import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 13Page_bt0_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-bt0_300.obj=6d3db5e306905991d140cfe463aaecca8be45633175a850cad41c241028597c3
    +test_classification:System
    +name: test_pcl5_highvalue_13page_bt0_300
    +test:
        +title: test_pcl5_highvalue_13page_bt0_300
        +guid:90b451f0-87dd-4af8-9e12-e232b6358f2a
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

def test_pcl5_highvalue_13page_bt0_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6d3db5e306905991d140cfe463aaecca8be45633175a850cad41c241028597c3', timeout=300)
    outputsaver.save_output()
