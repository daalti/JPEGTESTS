import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scsfangbd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scsfangbd.obj=f38d4bf9d6b234abee79ff36cb6e84ce154ee8305e2f22755af92c7f90335d12
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scsfangbd
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scsfangbd
        +guid:e40e1165-51f4-44b1-b423-8ca8df4ed55f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scsfangbd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f38d4bf9d6b234abee79ff36cb6e84ce154ee8305e2f22755af92c7f90335d12', timeout=600)
    outputsaver.save_output()
