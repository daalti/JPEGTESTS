import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_dirplan.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-dirplan.obj=86f13e760fdb8b568e89e974b853c5d99c5ccc5adf13d724c78e0b89c0e6ff94
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_dirplan
    +test:
        +title: test_pcl5_lowvaluenew_1page_dirplan
        +guid:c09e697b-ea49-4c77-9ac3-8d44c9aadb4c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_dirplan(setup_teardown, printjob, outputsaver):
    printjob.print_verify('86f13e760fdb8b568e89e974b853c5d99c5ccc5adf13d724c78e0b89c0e6ff94', timeout=600)
    outputsaver.save_output()
