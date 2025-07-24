import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pfhoriz2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pfhoriz2.obj=8bb23ed975fa0431475488d12a33b217e404e30d6aea142d1cb7c5d6a7af3b57
    +test_classification:System
    +name: test_pcl5_pcl_pcl_hpgl_pfhoriz2
    +test:
        +title: test_pcl5_pcl_pcl_hpgl_pfhoriz2
        +guid:fa4020b8-bf1b-47b4-b337-b61622f4e155
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pcl_hpgl_pfhoriz2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8bb23ed975fa0431475488d12a33b217e404e30d6aea142d1cb7c5d6a7af3b57', timeout=900)
    outputsaver.save_output()
