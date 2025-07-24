import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 42Page_refpoint.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:42Page-refpoint.obj=69c226ab0f33b2c7b74398e343a354ccf8b5c9e87c216ac845e56364ddd64506
    +test_classification:System
    +name: test_pcl5_lowvaluenew_42page_refpoint
    +test:
        +title: test_pcl5_lowvaluenew_42page_refpoint
        +guid:5aba1244-8b58-4ae8-b780-41b04a09dd83
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_42page_refpoint(setup_teardown, printjob, outputsaver):
    printjob.print_verify('69c226ab0f33b2c7b74398e343a354ccf8b5c9e87c216ac845e56364ddd64506', timeout=600)
    outputsaver.save_output()
