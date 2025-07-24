import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using rule5.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rule5.obj=0784400a02c4eb9e038cd1957a28e1a2d7c20de527b23925d40827dbc7fd29d2
    +test_classification:System
    +name: test_pcl5_pcl_printmod_rule5
    +test:
        +title: test_pcl5_pcl_printmod_rule5
        +guid:daaf46e4-cd7b-42d2-ae86-586120d3bd7d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_printmod_rule5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0784400a02c4eb9e038cd1957a28e1a2d7c20de527b23925d40827dbc7fd29d2', timeout=600)
    outputsaver.save_output()
