import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_indxplan.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-indxplan.obj=e8a1b33645c66c48d0cbd46879ac0054404a7c7003397e9cccd18029a56d0ba1
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_indxplan
    +test:
        +title: test_pcl5_lowvaluenew_1page_indxplan
        +guid:9f7d830a-c80c-4192-967b-ab1a9c86d56c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_indxplan(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e8a1b33645c66c48d0cbd46879ac0054404a7c7003397e9cccd18029a56d0ba1', timeout=600)
    outputsaver.save_output()
