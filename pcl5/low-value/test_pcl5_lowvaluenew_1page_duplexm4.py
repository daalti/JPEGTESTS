import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_duplexm4.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-duplexm4.obj=6f40c3f4608f089191d4d66f37b7b4012670da1c5e19f0f96eb3f443d412919b
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_duplexm4
    +test:
        +title: test_pcl5_lowvaluenew_1page_duplexm4
        +guid:958a992b-6977-4fd4-932a-501cae53876b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_duplexm4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6f40c3f4608f089191d4d66f37b7b4012670da1c5e19f0f96eb3f443d412919b', timeout=600)
    outputsaver.save_output()
