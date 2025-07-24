import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ppptest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ppptest.obj=b8180cb31f5b19d8b09bf03ded01288f74026da4bc4e15d9b462d9f136b92a92
    +test_classification:System
    +name: test_pcl5_pcl_cap_ppptest
    +test:
        +title: test_pcl5_pcl_cap_ppptest
        +guid:c1052472-c783-4cfd-80bf-490baae1f553
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cap_ppptest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b8180cb31f5b19d8b09bf03ded01288f74026da4bc4e15d9b462d9f136b92a92', timeout=600)
    outputsaver.save_output()
