import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 4Page_rasline2.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:4Page-rasline2.obj=9be64c121f618a66b47303ea54de58a5bbd464cf5da061164554856980e1e1c7
    +test_classification:System
    +name: test_pcl5_lowvaluenew_4page_rasline2
    +test:
        +title: test_pcl5_lowvaluenew_4page_rasline2
        +guid:5e6b1abe-b746-4d22-ae96-15842121befa
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_4page_rasline2(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('9be64c121f618a66b47303ea54de58a5bbd464cf5da061164554856980e1e1c7', timeout=300,expected_jobs=3)
    outputsaver.save_output()
