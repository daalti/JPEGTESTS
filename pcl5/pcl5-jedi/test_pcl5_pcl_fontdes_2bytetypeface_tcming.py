import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tcming.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tcming.obj=833a83396e674f1cad37d1a63c8eac0d541abfd41478e244cd8d9da30fa15e8c
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tcming
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tcming
        +guid:7ab033aa-29df-4acb-a8d1-737a8d2201e1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tcming(setup_teardown, printjob, outputsaver):
    printjob.print_verify('833a83396e674f1cad37d1a63c8eac0d541abfd41478e244cd8d9da30fa15e8c', timeout=600)
    outputsaver.save_output()
