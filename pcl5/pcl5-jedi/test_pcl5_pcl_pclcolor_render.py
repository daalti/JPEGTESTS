import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using render.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:800
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:render.obj=d8c7221c01f105a9d3139c00208fbfd05534b02b4e715e155ce55e3ef81d2a9d
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_render
    +test:
        +title: test_pcl5_pcl_pclcolor_render
        +guid:acbabf9b-a8fe-435e-ba4d-eafa907e36c0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_render( setup_teardown, printjob, outputsaver):
    printjob.print_verify('d8c7221c01f105a9d3139c00208fbfd05534b02b4e715e155ce55e3ef81d2a9d', timeout=800)
    outputsaver.save_output()