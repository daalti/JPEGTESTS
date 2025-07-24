import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 2selcmap.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2selcmap.obj=15b6614e4d1cc659fc176dfc880f9f86826c4deb4c31fa0332cef10ff00dd3fa
    +test_classification:System
    +name: test_pcl5_lowvaluenew_2selcmap
    +test:
        +title: test_pcl5_lowvaluenew_2selcmap
        +guid:c1596857-b5d2-4486-b6b0-81617b08106b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_2selcmap(setup_teardown, printjob, outputsaver):
    printjob.print_verify('15b6614e4d1cc659fc176dfc880f9f86826c4deb4c31fa0332cef10ff00dd3fa', timeout=600)
    outputsaver.save_output()
