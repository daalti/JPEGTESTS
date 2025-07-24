import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scsfangit.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scsfangit.obj=d7d62ec91c25ff9426e87f5946d3239d400788d8fd2046b795466394d1506e22
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scsfangit
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scsfangit
        +guid:314f1793-875d-4e56-a630-6f7061c2fe17
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scsfangit(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d7d62ec91c25ff9426e87f5946d3239d400788d8fd2046b795466394d1506e22', timeout=600)
    outputsaver.save_output()
