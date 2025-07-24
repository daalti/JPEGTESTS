import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using vector.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:vector.pcl=773ce98dfa49182b40d97ec6899afc783b1832728f078a8501a83407b8b22ee5
    +test_classification:System
    +name: test_pcl5_testfiles_vector_vector
    +test:
        +title: test_pcl5_testfiles_vector_vector
        +guid:da1a82d9-2d9f-4e5c-a06f-82ee5ea4cb73
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_vector_vector(setup_teardown, printjob, outputsaver):
    printjob.print_verify('773ce98dfa49182b40d97ec6899afc783b1832728f078a8501a83407b8b22ee5', timeout=600)
    outputsaver.save_output()
