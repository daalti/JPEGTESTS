import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 25Page_hmi.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:25Page-hmi.obj=beac9debee74ca52d743c2746c1ed7070c5638ef8ecd4af21c8e151b8ffa9a51
    +test_classification:System
    +name: test_pcl5_highvalue_25page_hmi
    +test:
        +title: test_pcl5_highvalue_25page_hmi
        +guid:1a2dea3a-230c-4698-947c-825d6ac0b79f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_25page_hmi(setup_teardown, printjob, outputsaver):
    printjob.print_verify('beac9debee74ca52d743c2746c1ed7070c5638ef8ecd4af21c8e151b8ffa9a51', timeout=600)
    outputsaver.save_output()
