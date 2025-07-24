import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fntdes10.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fntdes10.obj=a4999c03d3469bd281f7c16fa11c0f93fbd42ad01e85698a0440498aaaf999a0
    +test_classification:System
    +name: test_pcl5_pcl_fontf_if_fntdes10
    +test:
        +title: test_pcl5_pcl_fontf_if_fntdes10
        +guid:f54e14a7-81ef-4dea-828c-4f70852608e6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_if_fntdes10(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a4999c03d3469bd281f7c16fa11c0f93fbd42ad01e85698a0440498aaaf999a0', timeout=600)
    outputsaver.save_output()
