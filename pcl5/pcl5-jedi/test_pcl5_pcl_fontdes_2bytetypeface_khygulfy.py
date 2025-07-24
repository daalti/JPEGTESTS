import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygulfy.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygulfy.obj=e6973c92ef0406aab19c9f1d29b1a3213dd5deef80d9d780996ee6fd65208861
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygulfy
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygulfy
        +guid:7464b003-4cc0-498a-b30f-25aa8564e2b9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygulfy(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e6973c92ef0406aab19c9f1d29b1a3213dd5deef80d9d780996ee6fd65208861', timeout=600)
    outputsaver.save_output()
