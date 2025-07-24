import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 ufst using jvrtest_NoFont.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jvrtest_NoFont.obj=151846ce27b35eb389d4083b10bac18b701be182d7d5e883968d90333c9a62de
    +test_classification:System
    +name: test_pcl5_ufst_jvrtest_nofont
    +test:
        +title: test_pcl5_ufst_jvrtest_nofont
        +guid:20e6c159-d060-4af6-a8d0-0835a620ac53
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_ufst_jvrtest_nofont(setup_teardown, printjob, outputsaver):
    printjob.print_verify('151846ce27b35eb389d4083b10bac18b701be182d7d5e883968d90333c9a62de', timeout=600)
    outputsaver.save_output()
